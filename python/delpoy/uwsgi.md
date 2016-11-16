uWSGI and Nginx
===========

概念
-----

- WSGI: 是一种Web服务器网关接口。它是一个Web服务器（如nginx）与应用服务器（如uWSGI服务器）通信的一种规范。
- uWSGI: uWSGI是一个Web服务器，它实现了WSGI协议、uwsgi、http等协议。Nginx中HttpUwsgiModule的作用是与uWSGI服务器进行交换
- uwsgi: uwsgi协议是一个uWSGI服务器自有的协议，它用于定义传输信息的类型（type of information），每一个uwsgi packet前4byte为传输信息类型描述，它与WSGI相比是两样东西。

安装
----

更新源并且安装python开发相关库.
```python
sudo apt-get update
sudo apt-get install python-dev python-pip nginx
pip install uwsgi
```

在实际使用可以使用virtualenv创建单独的虚拟环境来安装 uwsgi

选项
---------
直接使用一份常用的ini格式的配置:
```
[uwsgi]
master=true      
socket=127.0.0.1:8000
home=/opt/ENV/collector; set PYTHONHOME/virtualenv
processes=4      
socket-timeout=300;为所有的socket操作设置内部超时时间（默认4秒
reload-mercy=10;设置在平滑的重启（直到接收到的请求处理完才重启）一个工作子进程中，等待这个工作结束的最长秒数
vacuum=true;当服务器退出的时候自动删除unix socket文件和pid文件
max-requests=1000;当一个工作进程处理的请求数达到这个值，那么该工作进程就会被回收重用（重启）
limit-as=1024 ;通过使用POSIX/UNIX的setrlimit()函数来限制每个uWSGI进程的虚拟内存使用数
listen=2024;设置socket的监听队列大小（默认:100）每一个socket都有一个相关联的队列，请求会被放入其中等待进程来处理。当这个队列满的时候，新来的请求就会被拒绝。
buffer-size=30000; 设置用于uwsgi包解析的内部缓存区大小,默认是4k.
daemonize=/var/log/uwsgi.log
memory-report=true
chdir=/opt/disk2/var/www/collector ; chdir to specified directory before apps loading
module=wsgi;加载指定的python WSGI模块. probably the mysite.wsgi module that startproject creates.
```

使用
--------------
以django部署举例

Django-specific options:
- chdir: The path to the directory that needs to be on Python’s import path – i.e., the directory containing the mysite package.
- module: The WSGI module to use – probably the mysite.wsgi module that startproject creates.
- env: Should probably contain at least DJANGO_SETTINGS_MODULE.
- home: Optional path to your project virtualenv.

Example ini configuration file:
```
[uwsgi]
chdir=/path/to/your/project
module=mysite.wsgi:application
master=True
pidfile=/tmp/project-master.pid
vacuum=True
max-requests=5000
daemonize=/var/log/uwsgi/yourproject.log
```

Example ini configuration file usage:
```
uwsgi --ini uwsgi.ini
```

nginx
----

```
server {
    listen                  80;
    charset                 utf-8;
    server_name localhost;
    access_log  /var/log/collector/access.log;
    error_log /var/log/collector/error.log;

    root /opt/disk2/var/www/collector;
    location / {
        root   /opt/disk2/var/www/collector;
        uwsgi_pass 127.0.0.1:8000;
        include    uwsgi_params;
    }

    location /static/ {
        expires 5d;
        alias /opt/disk2/var/www/collector/static/;
    }


location ^(.*)\.favicon.ico$ {
            log_not_found off;
            }
    location ~ /\.svn(.*)$ {
        deny  all;
    }
}

```

FAQ
---------
#### no python application found ...
如果uwsgi配置没错的话,可能就是django启动出错了,我这里是由于uwsgi是apache权限,而启动过程写的日志是root权限导致的.

#### django资源无法加载
看如下配置:
```
location /static/ {
    expires 5d;
    alias /opt/disk2/var/www/bale/static;
}
```
由于在static后少加了个/导致资源拼接路径成这样了:
```
 /bale/staticjs/browser.js
```



参考
----
- [How to use Django with uWSGI](https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/uwsgi/)
- [uWSGI其一：概念篇](http://www.nowamagic.net/academy/detail/1330331)
