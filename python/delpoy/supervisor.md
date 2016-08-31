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
redirect_stderr=true    
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
- ```redirect_stderr``` 重定向输出的日志

由于会写日志，所以我们需要确保```/var/log/time```目录的存在.

更详细的配置可以看[这里](http://supervisord.org/configuration.html#program-x-section-settings):
```
;[program:theprogramname]
;command=/bin/cat              ; the program (relative uses PATH, can take args)
;process_name=%(program_name)s ; process_name expr (default %(program_name)s)
;numprocs=1                    ; number of processes copies to start (def 1)
;directory=/tmp                ; directory to cwd to before exec (def no cwd)
;umask=022                     ; umask for process (default None)
;priority=999                  ; the relative start priority (default 999)
;autostart=true                ; start at supervisord start (default: true)
;autorestart=unexpected        ; whether/when to restart (default: unexpected)
;startsecs=1                   ; number of secs prog must stay running (def. 1)
;startretries=3                ; max # of serial start failures (default 3)
;exitcodes=0,2                 ; 'expected' exit codes for process (default 0,2)
;stopsignal=QUIT               ; signal used to kill process (default TERM)
;stopwaitsecs=10               ; max num secs to wait b4 SIGKILL (default 10)
;stopasgroup=false             ; send stop signal to the UNIX process group (default false)
;killasgroup=false             ; SIGKILL the UNIX process group (def false)
;user=chrism                   ; setuid to this UNIX account to run the program
;redirect_stderr=true          ; redirect proc stderr to stdout (default false)
;stdout_logfile=/a/path        ; stdout log path, NONE for none; default AUTO
;stdout_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
;stdout_logfile_backups=10     ; # of stdout logfile backups (default 10)
;stdout_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
;stdout_events_enabled=false   ; emit events on stdout writes (default false)
;stderr_logfile=/a/path        ; stderr log path, NONE for none; default AUTO
;stderr_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
;stderr_logfile_backups=10     ; # of stderr logfile backups (default 10)
;stderr_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
;stderr_events_enabled=false   ; emit events on stderr writes (default false)
;environment=A="1",B="2"       ; process environment additions (def no adds)
;serverurl=AUTO                ; override serverurl computation (childutils)
```

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
username = user ; Basic auth username
password = pass ; Basic auth password
```
然后可以使用浏览器打开ip:9001,如图
![图](http://7xk7ho.com1.z0.glb.clouddn.com/supervisor.png)


多进程
------------
当管理的进程会产生新的进程时, 会遇到执行完stop命令后子进程依然在:
这是我使用supervisor启动了一个django, 可以看到有俩进程.
```
www-data 14853  0.0  2.3  77856 24124 ?        S    17:17   0:00 /env/test/bin/python manage.py runserver 0:8888
www-data 14856  0.9  2.5 152548 25648 ?        Sl   17:17   0:04 /env/test/bin/python manage.py runserver 0:8888
```
当执行stop命令后, 如图:
```
www-data 14856  0.9  2.5 152548 25648 ?        Sl   17:17   0:05 /env/test/bin/python manage.py runserver 0:8888
```
为了关闭子进程， 这里需要介绍两个配置项 stopasgroup 和 killasgroup：
```
; 默认为 false，如果设置为 true，当进程收到 stop 信号时，会自动将该信号发给该进程的子进程。如果这个配置项为 true，那么也隐含 killasgroup 为 true。例如在 Debug 模式使用 Flask 时，Flask 不会将接收到的 stop 信号也传递给它的子进程，因此就需要设置这个配置项。
stopasgroup=false             ; send stop signal to the UNIX process 

; 默认为 false，如果设置为 true，当进程收到 kill 信号时，会自动将该信号发给该进程的子进程。如果这个程序使用了 python 的 multiprocessing 时，就能自动停止它的子线程。
killasgroup=false             ; SIGKILL the UNIX process group (def false)
```
所以当增加```stopasgroup=true```配置后， 父进程关闭子进程也就关掉了.

组管理
-----------------
```
[group:thegroupname]
programs=progname1,progname2  ; each refers to 'x' in [program:x] definitions
priority=999                  ; the relative start priority (default 999)
```
当添加了上述配置后，```progname1``` 和 ```progname2``` 的进程名就会变成 ```thegroupname:progname1``` 和 ```thegroupname:progname2``` 以后就要用这个名字来管理进程了，而不是之前的 ```progname1```.

以后执行``` supervisorctl stop thegroupname``` 就能同时结束 ```progname1``` 和 ```progname2```，执行 ```supervisorctl stop thegroupname:progname1``` 就能结束 ```progname1```


supervisorctl 命令介绍
------------------
```
# 停止某一个进程，program_name 为 [program:x] 里的 x
supervisorctl stop program_name
# 启动某个进程
supervisorctl start program_name
# 重启某个进程
supervisorctl restart program_name
# 结束所有属于名为 groupworker 这个分组的进程 (start，restart 同理)
supervisorctl stop groupworker:
# 结束 groupworker:name1 这个进程 (start，restart 同理)
supervisorctl stop groupworker:name1
# 停止全部进程，注：start、restart、stop 都不会载入最新的配置文件
supervisorctl stop all
# 载入最新的配置文件，停止原有进程并按新的配置启动、管理所有进程
supervisorctl reload
# 根据最新的配置文件，启动新配置或有改动的进程，配置没有改动的进程不会受影响而重启
supervisorctl update
```

开机自动启动 Supervisord
-------------------
如果是pip方式安装的话默认是没有被安装成服务，在ubuntu下可以这样来安装服务:
```
# 下载脚本
sudo su - root -c "sudo curl https://gist.githubusercontent.com/howthebodyworks/176149/raw/d60b505a585dda836fadecca8f6b03884153196b/supervisord.sh > /etc/init.d/supervisord"
# 设置该脚本为可以执行
sudo chmod +x /etc/init.d/supervisord
# 设置为开机自动运行
sudo update-rc.d supervisord defaults
# 试一下，是否工作正常
service supervisord stop
service supervisord start
```
注意：这个脚本下载下来后，还需检查一下与我们的配置是否相符合，比如默认的配置文件路径，pid 文件路径等，如果存在不同则需要进行一些修改

附录
-------

- 引用[monitoring-processes-with-supervisord](https://serversforhackers.com/monitoring-processes-with-supervisord)  
- [不错](http://my.oschina.net/crooner/blog/395069)
- [supervisord-tutorial](http://www.restran.net/2015/10/04/supervisord-tutorial/)
- [setting-supervisor-to-really-stop-django-runserver](https://coderwall.com/p/4tcw7w/setting-supervisor-to-really-stop-django-runserver)

注意
-------
- 在web界面查看log的时候， 好像只能显示指定数量的字符。
- print直接显示不出来的，需要sys.stdout.flush() [答案](http://stackoverflow.com/questions/13934801/supervisord-logs-dont-show-my-ouput)
- 在ubuntu下使用apt-get 方式安装可能是版本问题, 当启动的进程有子进程时stop时子进程无法关闭. 改为pip安装最新版然后配置一下服务的就可以了。