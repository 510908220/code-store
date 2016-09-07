# django调试之显示SQL语句

![](http://ocidwvtj2.bkt.clouddn.com/model_to_sql.png)

> 在使用```django```开发时，会经常与```Model```打交道. 简单复杂的语句都会写到，那么如何确保你写的```Model```语句和你想要的```SQL```语句是一样的呢. 举个例子,有如下```Model```:
```
class People(models.Model):
    class Meta:
        db_table = "people"
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
```
我想更新一下```name```字段,会写如下代码:
```
p = People.objects.get(name='xx')
p.name = 'oo'
p.save()
```
执行的```sql```语句是否真的符合预期？答案是:NO, 实际的sql语句是:
```
UPDATE people
SET "name" = "oo",
 "created" = "2016-09-07 15:10:41.362000"
WHERE
	"show_sql"."id" = '1'
```
虽然这句看起来使用没什么问题，但是却隐藏着bug. 可以看一下这篇[model-save-bug](https://github.com/510908220/code-store/blob/master/django/bug/model-save-bug.md?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io)

所以这里讲一下如何将```Model```的操作对应的```sql```语句打印出来，方便调试.

## SQL语句打印

#### 方式一
Queryset有一个query属性包含执行的sql语句,使用如下:
```
print MyModel.objects.filter(name="my name").query
```

#### 方式二
Django官网有一个[FAQ](https://docs.djangoproject.com/en/dev/faq/models/#how-can-i-see-the-raw-sql-queries-django-is-running)讲如何看```SQL```语句. 这里简单介绍一下. 

首选确保```DEBUG=True```,然后执行如下代码:
```
>>> from django.db import connection
>>> connection.queries
[{'sql': 'SELECT polls_polls.id, polls_polls.question, polls_polls.pub_date FROM polls_polls',
'time': '0.002'}]
```
```connection.queries```显示的是多次```Model```的操作. 如果想看某一次```Model```操作对应的```SQL```语句，可以先调用```reset_queries```函数（会清空connection.queries）

另外如果你正在使用多个数据库, 可以使用```connections ```:
```
>>> from django.db import connections
>>> connections['my_db_alias'].queries
```
#### 方式三
通过日志查看，可以增加如下日志, 有```django.db.backends```这个logger即可:
```
LOGGING = {
 
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

```

#### 方式四
[django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar) 是django调试的利器. 可以直接在页面上查看这次请求相关信息(sql语句、信号、日志、执行时间等). 这里简单介绍一下```django-debug-toolbar```是如何实现打印```SQL```语句的:

- 实现```cursor```相关接口, 在```execute```接口里执行完原有的逻辑后会记录```sql```相关信息.
- 替换掉```connection```的```cursor```属性

这种方式类似于```API HOOK```, 有兴趣可以看看源码.


