Supervisor使用
===========

> supervisor就是用Python开发的一套通用的进程管理程序，能将一个普通的命令行进程变为后台daemon，并监控进程状态，异常退出时能自动重启。


安装
-------

为了安装supervisord, 可以使用如下命令:  

`sudo apt-get install -y supervisor`

使用上述方式安装的好处是supervisord可以使用服务方式启动:

`sudo service supervisor start`

配置
-------
配置文件在目录`/etc/supervisor`.查看配置文件`/etc/supervisord/supervisord.conf`，有如下内容:
```
[include]
files = /etc/supervisor/conf.d/*.conf  /xxx/xxx/*.conf
```
所以任何在目录```/etc/supervisor/conf.d```内并且以```.conf```
结尾的都将被包含进来.
目录之间以空格分隔. 

现在来看一个简单的例子.监控的进程为currenttime.py,内容如下:
```python
import time
def t():
    while 1:
        time.sleep(5)
        print time.time()

if __name__ =='__main__':
    t()

```
首先创建一个配置文件```currenttime.conf```,这个文件位置在```/etc/supervisor/conf.d/currenttime.conf```:  

```
[program:currenttime]
command=/opt/env/sentry/bin/python  /home/studio/python/currenttime.py
directory=/home/studio/python
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/time/currenttime.err.log
stdout_logfile=/var/log/time/currenttime.out.log
user=www-data
```
通常，会用到下面一些选项:  

- ```[program:currenttime] ```定义要监控程序的名称,这里教它```currenttime``
- ```command```要运行的程序
- ```directory ```设置目录，Supervisord 在运行监控程序前会```"cd"```到这个目录
- ```autostart ```设置为"true"表示当Supervisord 启动时这个程序也会跟着启动
- ```autorestart ```如果设置为"true"，程序会重启当意外的退出.
- ```startretries ```尝试的次数，超过次数就会被认为失败了.
- ```stderr_logfile``` 程序错误的输出
- ```stdout_logfile ``` 程序输出
- ```user ``` 程序启动的用户
- ```environment ``` 传给程序的环境变量

由于会写日志，所以我们需要确保```/var/log/time```目录的存在.

进程控制
-------

现在我们已经配置好让Supervisord 去监控我们的currenttime进程,我们可以读取配置并且重新载入Supervisord，使用```supervisorctl ```:
```
supervisorctl reread
supervisorctl update
```

现在我们的currenttime进程应该运行了，可以通过```supervisorctl```查看:
```
$supervisorctl
currenttime                      RUNNING    pid 24788, uptime 0:09:05
```
也可以通过ps去查看:
```
$ps aux | grep currenttime
www-data 24788  0.0  0.3   9308  3716 ?        S    15:08   0:00 /opt/env/sentry/bin/python /home/studio/python/currenttime.py
```


我们可以使用`supervisorctl`做一些其他事情:

获取supervisorctl相关命令

`supervisor> help`

停止进程
`
supervisor> stop currenttime
currenttime: stopped
`

启动进程
```
supervisor> start currenttime
currenttime: started
```

也可以通过如下命令:
```
$ supervisorctl stop currenttime
$ supervisorctl start currenttime
```

Web管理
-------

还可以通过web方式去和Supervisord交互.通过web方式重启、通知、清除日志、查看输出。在```/etc/supervisord/supervisord.conf```增加如下内容:
```
[inet_http_server]
port = 0:9001
username = user # Basic auth username
password = pass # Basic auth password
```
然后可以使用浏览器打开ip:9001,如图
![图](http://7xk7ho.com1.z0.glb.clouddn.com/supervisor.png)


附录
-------

- 引用[monitoring-processes-with-supervisord](https://serversforhackers.com/monitoring-processes-with-supervisord)  
- [不错](http://my.oschina.net/crooner/blog/395069)

注意
-------
- 在web界面查看log的时候， 好像只能显示指定数量的字符。
- print直接显示不出来的，需要sys.stdout.flush() [答案](http://stackoverflow.com/questions/13934801/supervisord-logs-dont-show-my-ouput)
