消息队列之django-q源码学习
===========
> django-q 是一个多进程的任务队列的django app.


学习目的
------
了解一个消息队列的组成,  学习编码，最后能实现一个简单的消息队列.

架构
----
![](http://ocidwvtj2.bkt.clouddn.com/cluster.png)
下面对架构上列出的各个部分进行介绍.

#### Signed Task

所有的任务都是签名过的, 签名相关可以查看[signing](http://python.usyiyi.cn/django/topics/signing.html). 看个简单例子:
```python
>>> from django.core import signing
>>> value = signing.dumps({"foo": "bar"})
>>> value
'eyJmb28iOiJiYXIifQ:1NMg1b:zGcDE4-TCkaeGzLeW9UQwZesciI'
>>> signing.loads(value)
{'foo': 'bar'}
```

创建一个```Signed Task```很容易,看如下代码:
```
from django_q.tasks import async, result
async('math.copysign', 2, -2)
```
async会构造一个task, 然后签名，接着存入```Broker```队列. 由于是一个多进程队列，所以这里考虑可测试，通过配置添加```sync```参数来使任务同步执行.码如下:
```
def async(func, *args, **kwargs):
    """Queue a task for the cluster."""
    keywords = kwargs.copy()
    opt_keys = ('hook', 'group', 'save', 'sync', 'cached', 'iter_count', 'iter_cached', 'chain', 'broker')
    q_options = keywords.pop('q_options', {})
    # get an id
    tag = uuid()
    # build the task package
    task = {'id': tag[1],
            'name': keywords.pop('task_name', None) or q_options.pop('task_name', None) or tag[0],
            'func': func,
            'args': args}
    # push optionals
    for key in opt_keys:
        if q_options and key in q_options:
            task[key] = q_options[key]
        elif key in keywords:
            task[key] = keywords.pop(key)
    # don't serialize the broker
    broker = task.pop('broker', get_broker())
    # overrides
    if 'cached' not in task and Conf.CACHED:
        task['cached'] = Conf.CACHED
    if 'sync' not in task and Conf.SYNC:
        task['sync'] = Conf.SYNC
    # finalize
    task['kwargs'] = keywords
    task['started'] = timezone.now()
    # sign it
    pack = signing.SignedPackage.dumps(task)
    if task.get('sync', False):
        return _sync(pack)
    # push it
    broker.enqueue(pack)
    logger.debug('Pushed {}'.format(tag))
    return task['id']
```


#### Broker
消息队列, 保存django instances里创建的signed task. 如果消息队列支持消息回执(message receipts), 消息队列会保存着任务直到cluster确认任务处理了. <font color="red">如果在特定时间内任务没有确认，下次从消息队列取任务时还会取到这个任务.</font> 这样设计主要是为了保证至少有一个任务处理了. 
	
这里主要介绍一下以django model为后台存储的队列.

```
class ORM(Broker):
    @staticmethod
    def get_connection(list_key=Conf.PREFIX):
        if transaction.get_autocommit():  # Only True when not in an atomic block
            # Make sure stale connections in the broker thread are explicitly
            #   closed before attempting DB access.
            # logger.debug("Broker thread calling close_old_connections")
            db.close_old_connections()
        else:
            logger.debug("Broker in an atomic transaction")
        return OrmQ.objects.using(Conf.ORM)

    def queue_size(self):
        return self.get_connection().filter(key=self.list_key, lock__lte=_timeout()).count()

    def lock_size(self):
        return self.get_connection().filter(key=self.list_key, lock__gt=_timeout()).count()

    def purge_queue(self):
        return self.get_connection().filter(key=self.list_key).delete()

    def ping(self):
        return True

    def info(self):
        if not self._info:
            self._info = 'ORM {}'.format(Conf.ORM)
        return self._info

    def fail(self, task_id):
        self.delete(task_id)

    def enqueue(self, task):
        package = self.get_connection().create(key=self.list_key, payload=task, lock=_timeout())
        return package.pk

    def dequeue(self):
        tasks = self.get_connection().filter(key=self.list_key, lock__lt=_timeout())[0:Conf.BULK]
        if tasks:
            task_list = []
            lock = timezone.now()
            for task in tasks:
                task.lock = lock
                task.save(update_fields=['lock'])
                task_list.append((task.pk, task.payload))
            return task_list
        # empty queue, spare the cpu
        sleep(Conf.POLL)

    def delete_queue(self):
        return self.purge_queue()

    def delete(self, task_id):
        self.get_connection().filter(pk=task_id).delete()

    def acknowledge(self, task_id):
        return self.delete(task_id)
```

下面分析一下源码:

- get_connection: 获取消息队列对应的queryset, 这里采用了```using```语法，用在有多个数据库时选择相应的数据库. 
- _timeout: 返回一个当前时间减去超时时间的一个时间点. 为什么要这样呢, dequeue会详细说明.
- enqueue: 入队，创建任务时间点为_timeout()
- dequeue:出队，先取出时间小于_timeout()的任务，然后更新任务时间为当前时间。理解起来还是有点绕，如果改为这样看是不是清晰了呢:

```
def enqueue(self, task):
    package = self.get_connection().create(key=self.list_key, payload=task, lock=now())
    return package.pk

def dequeue(self):
    tasks = self.get_connection().filter(key=self.list_key, lock__lt=now())[0:Conf.BULK]
    if tasks:
        task_list = []
        lock = timezone.now()
        for task in tasks:
            task.lock = lock + Conf.retry
            task.save(update_fields=['lock'])
            task_list.append((task.pk, task.payload))
        return task_list
    # empty queue, spare the cpu
    sleep(Conf.POLL)
```
- acknowledge：确认任务执行完毕, 会将任务从队列移除.



#### Pusher
> pusher是作为一个进程不停的从broker里取任务, 取出的任务会检查签名是否正确, 然后放入进程队里里.
进程队列的大小可以配置的，当超过最大大小时,put函数会阻塞的. 下面分析一下源码:

```
def pusher(task_queue, event, broker=None):
    """
    Pulls tasks of the broker and puts them in the task queue
    :type task_queue: multiprocessing.Queue
    :type event: multiprocessing.Event
    """
    if not broker:
        broker = get_broker()
    logger.info(_('{} pushing tasks at {}').format(current_process().name, current_process().pid))
    while True:
        try:
            task_set = broker.dequeue()
        except Exception as e:
            logger.error(e)
            # broker probably crashed. Let the sentinel handle it.
            sleep(10)
            break
        if task_set:
            for task in task_set:
                ack_id = task[0]
                # unpack the task
                try:
                    task = signing.SignedPackage.loads(task[1])
                except (TypeError, signing.BadSignature) as e:
                    logger.error(e)
                    broker.fail(ack_id)
                    continue
                task['ack_id'] = ack_id
                task_queue.put(task)
            logger.debug(_('queueing from {}').format(broker.list_key))
        if event.is_set():
            break
    logger.info(_("{} stopped pushing tasks").format(current_process().name))
```
参数event是一个Event类型的，主要是用于主进程通知push退出的. 


#### Worker
> 从进程队列里取任务,然后去执行，然后将结果存入任务队列里. 下面分析一下源码:

```python
def worker(task_queue, result_queue, timer, timeout=Conf.TIMEOUT):
    """
    Takes a task from the task queue, tries to execute it and puts the result back in the result queue
    :type task_queue: multiprocessing.Queue
    :type result_queue: multiprocessing.Queue
    :type timer: multiprocessing.Value
    """
    name = current_process().name
    logger.info(_('{} ready for work at {}').format(name, current_process().pid))
    task_count = 0
    # Start reading the task queue
    for task in iter(task_queue.get, 'STOP'): # STOP用于告诉进程退出
        result = None
        timer.value = -1  # Idle
        task_count += 1
        # Get the function from the task
        logger.info(_('{} processing [{}]').format(name, task['name']))
        f = task['func']
        # if it's not an instance try to get it from the string
        if not callable(task['func']):
            try:
                module, func = f.rsplit('.', 1)
                m = importlib.import_module(module)
                f = getattr(m, func)
            except (ValueError, ImportError, AttributeError) as e:
                result = (e, False)
                if rollbar:
                    rollbar.report_exc_info()
        # We're still going
        if not result:
            db.close_old_connections()
            # execute the payload
            timer.value = task['kwargs'].pop('timeout', timeout or 0)  # Busy
            try:
                res = f(*task['args'], **task['kwargs'])
                result = (res, True)
            except Exception as e:
                result = ('{}'.format(e), False)
                if rollbar:
                    rollbar.report_exc_info()
        # Process result
        task['result'] = result[0]
        task['success'] = result[1]
        task['stopped'] = timezone.now()
        result_queue.put(task)
        timer.value = -1  # Idle
        # Recycle
        if task_count == Conf.RECYCLE:
            timer.value = -2  # Recycled
            break
    logger.info(_('{} stopped doing work').format(name))
```

参数说明:

- task_queue: 进程任务队列
- result_queue: 结果进程队列
- timer: 是multiprocessing.Value类型的, 主要是用于记录任务执行的时间，这样主进程会根据这个值以及任务执行时间来判断是否超时.
- timeout:worker执行一个任务最大时间，超过这个时间worker会被重启



#### Monitor

> 检查结果队列, 将队列包容保存到django数据库. 如果broker支持消息回执，保存完结果后会进行确认. 这样就可以从消息队列移除这个任务了。就看一下源码:

```
def monitor(result_queue, broker=None):
    """
    Gets finished tasks from the result queue and saves them to Django
    :type result_queue: multiprocessing.Queue
    """
    if not broker:
        broker = get_broker()
    name = current_process().name
    logger.info(_("{} monitoring at {}").format(name, current_process().pid))
    for task in iter(result_queue.get, 'STOP'):
        # save the result
        if task.get('cached', False):
            save_cached(task, broker)
        else:
            save_task(task, broker)
        # acknowledge and log the result
        if task['success']:
            # acknowledge
            ack_id = task.pop('ack_id', False)
            if ack_id:
                broker.acknowledge(ack_id)
            # log success
            logger.info(_("Processed [{}]").format(task['name']))
        else:
            # log failure
            logger.error(_("Failed [{}] - {}").format(task['name'], task['result']))
    logger.info(_("{} stopped monitoring results").format(name))
```


#### Sentinel
> 从字面意思看是"哨兵"的意思. 负责产生所有的进程(pusher、monitor、worker)，并检查各个进程健康状态. worker进程的话会额外检查执行超时并重启之. 其他进程会会检查是否存活，不存活的话会重启. 

这里涉及很多进程操作,在构造函数里有如下设置:
```python
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_DFL)
```

常用信号如下:

| 信号          | 含义     | 描述   | 
| ------------- |:---------| :------|
|SIGINT |   终止进程  |   中断进程  (control+c)
|SIGTERM |  终止进程  |   软件终止信号(kill pid)
|SIGKILL |  终止进程   |  杀死进程
|SIGALRM |  闹钟信号|


这句具体含义有如下解释:
```
signal.signal(signal.SIGINT, signal.SIG_IGN)
```
这句忽略了```control+c```

```
signal.signal(signal.SIGTERM, signal.SIG_DFL)
```

给信号```SIGTERM```设置一个默认的处理.


qcluster
---------

```
class Cluster(object):
    def __init__(self, broker=None):
        self.broker = broker or get_broker()
        self.sentinel = None
        self.stop_event = None
        self.start_event = None
        self.pid = current_process().pid
        self.host = socket.gethostname()
        self.timeout = Conf.TIMEOUT
        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)

    def start(self):
        # Start Sentinel
        self.stop_event = Event()
        self.start_event = Event()
        self.sentinel = Process(target=Sentinel,
                                args=(self.stop_event, self.start_event, self.broker, self.timeout))
        self.sentinel.start()
        logger.info(_('Q Cluster-{} starting.').format(self.pid))
        while not self.start_event.is_set():
            sleep(0.1)
        return self.pid

    def stop(self):
        if not self.sentinel.is_alive():
            return False
        logger.info(_('Q Cluster-{} stopping.').format(self.pid))
        self.stop_event.set()
        self.sentinel.join()
        logger.info(_('Q Cluster-{} has stopped.').format(self.pid))
        self.start_event = None
        self.stop_event = None
        return True

    def sig_handler(self, signum, frame):
        logger.debug(_('{} got signal {}').format(current_process().name,
                                                  Conf.SIGNAL_NAMES.get(signum, 'UNKNOWN')))
        self.stop()

    @property
    def stat(self):
        if self.sentinel:
            return Stat.get(self.pid)
        return Status(self.pid)

    @property
    def is_starting(self):
        return self.stop_event and self.start_event and not self.start_event.is_set()

    @property
    def is_running(self):
        return self.stop_event and self.start_event and self.start_event.is_set()

    @property
    def is_stopping(self):
        return self.stop_event and self.start_event and self.start_event.is_set() and self.stop_event.is_set()

    @property
    def has_stopped(self):
        return self.start_event is None and self.stop_event is None and self.sentinel
```

这里创建sentinel进程时和一般的有点不一样, 指定的是一个Sentinel对象，对象在__init__.py时执行了相应的逻辑.这应该算一个技巧了. 一般是传入一个可调用对象，这里相当于是调用了构造函数，在构造函数里执行了一般可调用对象的逻辑.



问题
-------

里面看到了一些数据库相关的操作.有点疑惑. 这里记录一下:
- transaction.get_autocommit():

```
class ConnectionHandler(object):
    def __init__(self, databases=None):
        """
        databases is an optional dictionary of database definitions (structured
        like settings.DATABASES).
        """
        self._databases = databases
        self._connections = local()
```

http://stackoverflow.com/questions/34695052/how-is-django-persistent-database-connections-thread-safe
