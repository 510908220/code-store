# jenkins接口之python

jenkins不仅功能强大,而且还有对外开放的api接口,更是如虎添翼.  官方文档[Remote access API](https://wiki.jenkins-ci.org/display/JENKINS/Remote+access+API) 提供了详细的使用说明. 这里主要是介绍python对jenkins api的实现版本.

## Python Jenkins

[Python Jenkins](http://python-jenkins.readthedocs.io/en/latest/) 是一个python对jenkins REST API的包装. 提供一种pythonic的方式与jenkins 服务进行交互. 有很多易于使用的接口:

- 创建新的job
- 拷贝已有的job
- 删除job
- 更新job
- 获取一个job构建信息
- 获取jenkins插件信息
- 触发job构建
- 创建nodes
- 打开/关闭 nodes
- 获取nodes信息
- 创建/删除视图
- 关闭jenkins
- 获取构建中的列表
- 设置下次构建号
- 安装插件
- 其他

## 常用接口说明

在使用前需要创建一个`Jenkins`对象
```python
import jenkins  
server = jenkins.Jenkins('http://localhost:8080')
```

##### 获取job数量
`server.jobs_count()`


#####获取所有的job  
`server.get_jobs()`

#####获取远程构建url
`server.build_job_url(job_name, params, token)`
其中`params`为传给构建的参数.

#####创建job
`server.create_job('empty', jenkins.EMPTY_CONFIG_XML)`,可以根据配置创建job，这样可以通过基本批量创建job

#####获取指定job信息
`server.get_job_info('aliyun')`,这里换成自己名字即可,说一下返回值:

- color  

|颜色        |含义 |
|------------|----|
| red        |构建失败    |
| blue       |构建成功    |
| aborted    |取消构建    |
| notbuilt   |在第一次构建时获取到的，触发构建后就变成其他颜色了    |
| xxx_anime  |xxx表示red或者blue或者aborted,如果上一次构建成功， 那么这次就是blue_anime，依次类推)|

- lastCompletedBuild:上一次构建信息
- lastBuild:上一次构建信息
- lastUnsuccessfulBuild: 上次不成功的构建(可能是取消或者失败)
- lastFailedBuild:上一次失败构建
- lastSuccessfulBuild:上一次成功构建
- lastStableBuild:感觉与lastSuccessfulBuild一样
- builds:历史构建列表
- firstBuild:第一次构建信息
- url:这个job的url
- healthReport:构建报告，比如多少次失败等
- nextBuildNumber:下一次构建号  

	当第一次触发构建的时候，当颜色状态为`notbuilt`时，获取到的`lastBuild`为`None`

## 构建各个阶段

#####第一次构建

```
scm --- {}
color --- red
lastSuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}
actions --- []
lastCompletedBuild --- {u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}
lastUnsuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}
upstreamProjects --- []
lastFailedBuild --- {u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}
healthReport --- [{u'iconUrl': u'health-20to39.png', u'score': 40, u'description': u'Build stability: 3 out of the last 5 builds failed.', u'iconClassName': u'icon-health-20to39'}]
queueItem --- None
lastBuild --- {u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}
lastStableBuild --- {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}
description --- 
downstreamProjects --- []
concurrentBuild --- False
lastUnstableBuild --- None
buildable --- True
displayNameOrNull --- None
inQueue --- False
keepDependencies --- False
name --- aliyun
displayName --- aliyun
builds --- [{u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}, {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}, {u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}, {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}, {u'url': u'http://localhost:8080/job/aliyun/8/', u'number': 8}, {u'url': u'http://localhost:8080/job/aliyun/7/', u'number': 7}, {u'url': u'http://localhost:8080/job/aliyun/6/', u'number': 6}, {u'url': u'http://localhost:8080/job/aliyun/5/', u'number': 5}, {u'url': u'http://localhost:8080/job/aliyun/4/', u'number': 4}, {u'url': u'http://localhost:8080/job/aliyun/3/', u'number': 3}, {u'url': u'http://localhost:8080/job/aliyun/2/', u'number': 2}, {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}]
firstBuild --- {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}
url --- http://localhost:8080/job/aliyun/
nextBuildNumber --- 13
property --- []
```
warning:可以看到color值notbuilt,lastBuild值为None

#####正在构建

```
scm --- {}
color --- blue_anime
lastSuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}
actions --- []
lastCompletedBuild --- {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}
lastUnsuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/8/', u'number': 8}
upstreamProjects --- []
lastFailedBuild --- {u'url': u'http://localhost:8080/job/aliyun/8/', u'number': 8}
healthReport --- [{u'iconUrl': u'health-40to59.png', u'score': 60, u'description': u'Build stability: 2 out of the last 5 builds failed.', u'iconClassName': u'icon-health-40to59'}]
queueItem --- None
lastBuild --- {u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}
lastStableBuild --- {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}
description --- 
downstreamProjects --- []
concurrentBuild --- False
lastUnstableBuild --- None
buildable --- True
displayNameOrNull --- None
inQueue --- False
keepDependencies --- False
name --- aliyun
displayName --- aliyun
builds --- [{u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}, {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}, {u'url': u'http://localhost:8080/job/aliyun/8/', u'number': 8}, {u'url': u'http://localhost:8080/job/aliyun/7/', u'number': 7}, {u'url': u'http://localhost:8080/job/aliyun/6/', u'number': 6}, {u'url': u'http://localhost:8080/job/aliyun/5/', u'number': 5}, {u'url': u'http://localhost:8080/job/aliyun/4/', u'number': 4}, {u'url': u'http://localhost:8080/job/aliyun/3/', u'number': 3}, {u'url': u'http://localhost:8080/job/aliyun/2/', u'number': 2}, {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}]
url --- http://localhost:8080/job/aliyun/
firstBuild --- {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}
nextBuildNumber --- 11
property --- []
```

#####构建成功
```
scm --- {}
color --- blue
lastSuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}
actions --- []
lastCompletedBuild --- {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}
lastUnsuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}
upstreamProjects --- []
lastFailedBuild --- {u'url': u'http://localhost:8080/job/aliyun/8/', u'number': 8}
healthReport --- [{u'iconUrl': u'health-40to59.png', u'score': 60, u'description': u'Build stability: 2 out of the last 5 builds failed.', u'iconClassName': u'icon-health-40to59'}]
queueItem --- None
lastBuild --- {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}
lastStableBuild --- {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}
description --- 
downstreamProjects --- []
concurrentBuild --- False
lastUnstableBuild --- None
buildable --- True
displayNameOrNull --- None
inQueue --- False
keepDependencies --- False
name --- aliyun
displayName --- aliyun
builds --- [{u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}, {u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}, {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}, {u'url': u'http://localhost:8080/job/aliyun/8/', u'number': 8}, {u'url': u'http://localhost:8080/job/aliyun/7/', u'number': 7}, {u'url': u'http://localhost:8080/job/aliyun/6/', u'number': 6}, {u'url': u'http://localhost:8080/job/aliyun/5/', u'number': 5}, {u'url': u'http://localhost:8080/job/aliyun/4/', u'number': 4}, {u'url': u'http://localhost:8080/job/aliyun/3/', u'number': 3}, {u'url': u'http://localhost:8080/job/aliyun/2/', u'number': 2}, {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}]
url --- http://localhost:8080/job/aliyun/
firstBuild --- {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}
nextBuildNumber --- 12
property --- []
```

#####取消构建
```
scm --- {}
color --- aborted
lastSuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}
actions --- []
lastCompletedBuild --- {u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}
lastUnsuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}
upstreamProjects --- []
lastFailedBuild --- {u'url': u'http://localhost:8080/job/aliyun/8/', u'number': 8}
healthReport --- [{u'iconUrl': u'health-40to59.png', u'score': 60, u'description': u'Build stability: 2 out of the last 5 builds failed.', u'iconClassName': u'icon-health-40to59'}]
queueItem --- None
lastBuild --- {u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}
lastStableBuild --- {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}
description --- 
downstreamProjects --- []
concurrentBuild --- False
lastUnstableBuild --- None
buildable --- True
displayNameOrNull --- None
inQueue --- False
keepDependencies --- False
name --- aliyun
displayName --- aliyun
builds --- [{u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}, {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}, {u'url': u'http://localhost:8080/job/aliyun/8/', u'number': 8}, {u'url': u'http://localhost:8080/job/aliyun/7/', u'number': 7}, {u'url': u'http://localhost:8080/job/aliyun/6/', u'number': 6}, {u'url': u'http://localhost:8080/job/aliyun/5/', u'number': 5}, {u'url': u'http://localhost:8080/job/aliyun/4/', u'number': 4}, {u'url': u'http://localhost:8080/job/aliyun/3/', u'number': 3}, {u'url': u'http://localhost:8080/job/aliyun/2/', u'number': 2}, {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}]
url --- http://localhost:8080/job/aliyun/
firstBuild --- {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}
nextBuildNumber --- 11
property --- []
```

#####构建失败
```
scm --- {}
color --- red
lastSuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}
actions --- []
lastCompletedBuild --- {u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}
lastUnsuccessfulBuild --- {u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}
upstreamProjects --- []
lastFailedBuild --- {u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}
healthReport --- [{u'iconUrl': u'health-20to39.png', u'score': 40, u'description': u'Build stability: 3 out of the last 5 builds failed.', u'iconClassName': u'icon-health-20to39'}]
queueItem --- None
lastBuild --- {u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}
lastStableBuild --- {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}
description --- 
downstreamProjects --- []
concurrentBuild --- False
lastUnstableBuild --- None
buildable --- True
displayNameOrNull --- None
inQueue --- False
keepDependencies --- False
name --- aliyun
displayName --- aliyun
builds --- [{u'url': u'http://localhost:8080/job/aliyun/12/', u'number': 12}, {u'url': u'http://localhost:8080/job/aliyun/11/', u'number': 11}, {u'url': u'http://localhost:8080/job/aliyun/10/', u'number': 10}, {u'url': u'http://localhost:8080/job/aliyun/9/', u'number': 9}, {u'url': u'http://localhost:8080/job/aliyun/8/', u'number': 8}, {u'url': u'http://localhost:8080/job/aliyun/7/', u'number': 7}, {u'url': u'http://localhost:8080/job/aliyun/6/', u'number': 6}, {u'url': u'http://localhost:8080/job/aliyun/5/', u'number': 5}, {u'url': u'http://localhost:8080/job/aliyun/4/', u'number': 4}, {u'url': u'http://localhost:8080/job/aliyun/3/', u'number': 3}, {u'url': u'http://localhost:8080/job/aliyun/2/', u'number': 2}, {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}]
url --- http://localhost:8080/job/aliyun/
firstBuild --- {u'url': u'http://localhost:8080/job/aliyun/1/', u'number': 1}
nextBuildNumber --- 13
proper ty --- []
```

## 使用注意


下面代码是修改jenkins里shell命令脚本:

```python
server = jenkins.Jenkins(URL)
info = server.get_job_config("pamc-web_10.7.108.10")
config = xmltodict.parse(info)
config["project"]["builders"]["hudson.tasks.Shell"]["command"] += u"\ndate;"
new_config =  xmltodict.unparse(config, pretty=True)
server.reconfig_job("pamc-web_10.7.108.10",new_config)
```

这里需要注意的是reconfig_job参数, 第一个参数是非unicode,第二个参数是unicode,具体看一下reconfig_job源码就知道了. 如果安全设置里有如下配置:
![](http://ocidwvtj2.bkt.clouddn.com/crumb.png)
那么会导致请求头里有```u'.Crumb: 83f6b2d57d269d535133c7bcad4e15a7'```这一项，会导致
```python
  File "C:\Python27\lib\httplib.py", line 1055, in endheaders
    self._send_output(message_body)
  File "C:\Python27\lib\httplib.py", line 897, in _send_output
    msg += message_body
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe5 in position 1217: ordinal not in range(128)
```
简单解决去掉这项配置即可. 另外需要<font color=red>注意,jenkins里的shell如果是ssh的话, 对应的配置类似于这样:```config["project"]["builders"]["org.jvnet.hudson.plugins.SSHBuilder"]```</font>