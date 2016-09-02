# 一个由于django model的save引起的bug


## 执行环境

##### 数据模型
实现一个对一些主机的程序部署, 有如下Model:

```
class Host(models.Model):
    class Meta:
        db_table = "hosts"
    
    STATUS = Choices(
        ('new', 'new'),
        ('running', 'running'),
        ('success', 'success'),
        ('fail', 'fail'),
    )
    AGENT_STATUS = Choices(
        ('online', 'online'),
        ('offline', 'offline'),
    )
    ip = models.CharField(
        max_length=200, unique=True, blank=False, null=False)
    deploy_version = models.CharField(max_length=200, blank=True, null=True, default="")
    remote_version = models.CharField(max_length=200, blank=True, null=True, default="")
    log = models.TextField(blank=True)
    agent_status = models.CharField(max_length=20, choices=AGENT_STATUS, default=AGENT_STATUS.offline)
    last_agent_detection = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS.new)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.ip
```

简单介绍一下相关字段:
- ip: 要部署程序的主机
- deploy_version:当前需要部署的版本号
- remote_version: 远程主机的版本号
- agent_status:远程主机上执行部署动作代理是否在线
- status:部署操作执行状态

##### 状态修改
有两个进程(django后台进程)会修改模型字段:

######1. deploy.py
这个进程主要是执行具体的部署操作, 代码如下:

```
def host_process(host):
    deploy_logger.info("start deploy ip is:%s, deploy version is:%s", host.ip, host.deploy_version)
    cl = client.Client(host.ip, 8000, host.deploy_version)
    
    # 标记开始部署
    host.status = Host.STATUS.running
    host.save()
    
    success, log = cl.deply()
    
    # 部署结束,设置部署返回信息
    if success:
        host.remote_version = host.deploy_version
        host.status = Host.STATUS.success
    else:
        host.status = Host.STATUS.fail
    host.log = log
    host.save()
```
######2. heartbeat.py
这个进程主要是检测在远程主机上部署的代理状态.
```
def heartbeat_detection(host):
    cl = client.Client(host.ip, 8000, host.deploy_version)
    online, log = cl.is_ok()
    if not online:
        host.agent_status = Host.AGENT_STATUS.offline
    else:
        host.agent_status = Host.AGENT_STATUS.online
    host.save()  
   
```

其中
- ```host_process```主要是更新```remote_version```和```status```字段.
- ```heartbeat_detection```主要是更新```agent_status```字段.

## bug现象

&#160;&#160;&#160;&#160;当我开始部署程序时, 部署成功时```remote_version```和```deploy_version```相等并且```status```值为```success```. 但是过了一下```remote_version```和```status```值又变成其他的了. 而且还可能持续的变化. 

&#160;&#160;&#160;&#160;为什么会这样呢? 反复看代码发现只有```host_process```会修改```remote_version```和```status```字段, 也查看了机器上没有其他额外的```deploy```脚本在执行. 反复的找还是没头绪，后来想到看一下```django```的日志输出:
```
UPDATE `hosts` SET `ip` = '10.6.0.231', `deploy_version` = '1.0.0.6', `remote_version` = '1.0.0.5', `log` = '', `agent_status` = 'online', `last_agent_detection` = '2016-09-01 15:01:43', `status` = 'running', `created` = '2016-08-30 17:40:47', `updated` = '2016-09-01 15:01:43' WHERE `hosts`.`id` = 2; 
```
看完日志我就恍然大悟了，原来```save```方法是全字段更新, 这样问题就很明显了. ```host_process```和 ```heartbeat_detection``` 都会执行一个全部更新的sql语句. 这样就会导致数据的覆盖. 所以会看到值在不断的变化.

## bug解决
其实```save```方法有一个参数是```update_fields```可以指定更新哪些字段. 在更新数据显示指定要更新的数据就不会有这样的问题了. 


## 建议

- 打开日志:
在调试django时指定一个名为```django```的logger, 类似这样:
```
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "default.log"),  
            'maxBytes': 1024 * 1024 * 5,  
            'backupCount': 5, 
            'formatter': 'standard',  
        },
    'loggers': {
        'django': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': False
        },
```
这样可以把model操作对应的sql写入到日志, 排查问题时可以看到对应的操作到底是什么sql.

-  使用debug_toolbar:
可以在调试模式下加入```debug_toolbar```这个app, 这样可以在页面上看到view处理函数操作model时对应的sql语句. 对于那些不返回页面的view直接是无法看到对应sql的,不过是有解决方案的,通过中间件实现.可以参考[How to use django-debug-toolbar for django-tastypie](http://stackoverflow.com/questions/14618203/how-to-use-django-debug-toolbar-for-django-tastypie)