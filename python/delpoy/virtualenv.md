# 虚拟环境virtualenv



## 概述

&emsp;&emsp;virtualenv 是一个用来创建独立的 python 环境的工具，用来解决依赖、版本以及权限
问题。比如，在一个项目中你需要 libFoo1.0 版本，在另外一个项目中，你依赖 libFoo2.0，
那么你怎么同时使用这二个项目呢，如果你同时安装 libFoo1.0 和 libFoo2.0 到系统目录```/usr/lib/python2.7/site-packages/```中，总会有一个不可运行。  
&emsp;&emsp;另外，如果你没有权限在全局的 site-packages 中安装 python 库的时候怎么办。  
&emsp;&emsp;在上面这些场景中， virtualenv 可以帮助你很好的解决这些问题。 virtualenv 可以创建
一个虚拟环境，它拥有自己的独立安装目录，不会影响其它虚拟环境和全局环境。


## 基本使用

首先进行安装```pip install virtualenv```,详细查看[installation](https://virtualenv.pypa.io/en/stable/installation/)


在确认安装成功后，我们就可以开始使用 virtualenv 来管理我们的 python 环境。最
基本的用法就是:  

```
root@wq-native-22-5-1-69:~# cd /opt/env/
root@wq-native-22-5-1-69:/opt/env# virtualenv test
New python executable in /opt/env/test/bin/python
Installing setuptools, pip, wheel...done.
root@wq-native-22-5-1-69:/opt/env# ls
lint  test
root@wq-native-22-5-1-69:/opt/env# cd test/
root@wq-native-22-5-1-69:/opt/env/test# ls
bin  include  lib  local  pip-selfcheck.json
root@wq-native-22-5-1-69:/opt/env/test# 
```


执行这条命令后， virtualenv 就会创建一个名为```test```的目录，并且安装了```/opt/env/test/bin/python```，创建了 lib,bin,include,local 目录以及安装 pip. 在test目录下，你安装的python库都会放入test/lib下，而且默认的 python 会是```/opt/env/test/bin/python ```
</br>
我们已经创建了test这个虚拟环境，但默认使用的还是全局的 python 环境，我们需要使用如下命令激活指定的虚拟环境:

```
root@wq-native-22-5-1-69:/opt/env# cd test/
root@wq-native-22-5-1-69:/opt/env/test# source ./bin/activate
(test) root@wq-native-22-5-1-69:/opt/env/test# which python
/opt/env/test/bin/python
(test) root@wq-native-22-5-1-69:/opt/env/test# 

```
在执行了```source ./bin/activate```后，就激活了当前的虚拟环境，可以看到终端提示也发生了改变，提示我们已经在一个虚拟环境中。  
</br>
在使用完虚拟 环境后，我们应该关闭当前的 虚拟环境，使用命令 deactive:
```
(test) root@wq-native-22-5-1-69:/opt/env/test# deactivate 
root@wq-native-22-5-1-69:/opt/env/test# 

```

## 最佳实践

#####指定 python 版本  
&emsp;&emsp;首先，对于文章开始的问题，最好的解决方案就是创建一个python2.7的虚拟环境，在这个虚拟环境下使用py2.7依赖的框架。这样就不必修改全局的 python，避免造成系统
其它问题。而且，不需要修改原来的程序，强行指定使用自己安装的 python。  
&emsp;&emsp;对于指定 python 版本，可以使用 -p PYTHON_EXE, –python=PYTHON_EXE 来指定python 程序。  
```
liuchang@ubuntu:~$ virtualenv -p /usr/bin/python3.4 ENV3.4
Running virtualenv with interpreter /usr/bin/python3.4
Using base prefix '/usr'
New python executable in ENV3.4/bin/python3.4
Also creating executable in ENV3.4/bin/python
Installing setuptools, pip...done.
liuchang@ubuntu:~$ cd ENV3.4/
liuchang@ubuntu:~/ENV3.4$ source ./bin/activate
(ENV3.4)liuchang@ubuntu:~/ENV3.4$ python --version
Python 3.4.0
```
&emsp;&emsp;可以看到，我们创建了一个 ENV，默认的 python 版本已经是 3.4。  
* 生成可打包的环境  
&emsp;&emsp;其次，在某种特殊的需求下，可能没有网络，我们期望直接打包一个 ENV，可以解压
后直接使用。这时候可以使用 virtualenv –relocatable 指令将一个 ENV 修改为可更改位
置的 ENV。  
```
liuchang@ubuntu:~/ENV3.4$ virtualenv --relocatable ./
Making script ./bin/pip3 relative
Making script ./bin/easy_install relative
Making script ./bin/easy_install-3.4 relative
Making script ./bin/pip relative
Making script ./bin/pip3.4 relative
```
&emsp;&emsp;当前的 ENV 相关的可执行文件都被修改为相对路径，你可以打包当前目录，上传到其
它位置直接使用。  
* 默认环境变量和配置文件
&emsp;&emsp;在上面，我们讲了指定 python 版本的方法，但是如果每次生成 virtualenv 都需要手
动指定还是比较麻烦的，我们可以通过二种办法来指定默认配置, 分别为环境变量和配置文
件。  
  * 环境变量  
&emsp;&emsp;对于每个命令行参数，都会先查找环境变量是否已经指定。比如 –python 参数，会先
查看 VIRTUALENV_PYTHON。  
&emsp;&emsp;环境变量的形式为：对于命令行参数，变换为大写，并将减号替换为下划线，例如对于
参数 –foo-bar，对应的环境变量就是 VIRTUALENV_FOO_BAR。  
```
$ export VIRTUALENV_PYTHON=/opt/python-3.3/bin/python
$ virtualenv ENV
```
  * 配置文件  
&emsp;&emsp;virtualenv 也会检查相关的配置文件，在 *nix 系统上，配置文件为 $HOME/.virtualenv/
virtualenv.ini，在 Windows 上，则 j 是%APPDATA%/virtualenv/virtualenv.ini. 示例如
下：  
```
[virtualenv]
python = /opt/python-3.3/bin/python
```

高级用法
--------
* bootstrap 脚本  
&emsp;&emsp;在使用 virtualenv 命令创建了一个 ENV 后，它只会生成一个 ENV，生成必要的目录
文件。一般情况下，我们还要拉取代码，安装常用库等操作。  
&emsp;&emsp;virtualenv 支持自定义的 bootstrap 脚本，在生成 ENV 的时候，完成一些自定义的操
作。  
&emsp;&emsp;virtualenv 的 bootstrap 脚本通过钩子（ HOOK）的形式来支持自定义，钩子函数分
别是:  
&emsp;&emsp;1. extend_parser(optparse_parser) 拓展 virtualenv 的命令行解析  
&emsp;&emsp;2. adjust_options(options, args) 调整命令行参数值  
&emsp;&emsp;3. after_install(options, home_dir) 在生成 ENV 后执行  
&emsp;&emsp;最经常使用的钩子函数就是 after_install，通过这个函数，我们可以执行很多操作。一个示
例如下：  
``` python
def after_install(options, home_dir):
    if sys.platform == 'win32':
        bin = 'Scripts'
    else:
        bin = 'bin'
    subprocess.call([join(home_dir, bin, 'easy_install'),
    'MyPackage'])
    subprocess.call([join(home_dir, bin, 'my-package-script'),
    'setup', home_dir])
```

virtualenvwrapper
--------
#####安装
pip install virtualenvwrapper
安装完成后， 会在下面的位置生成virtualwrapper的shell脚本:
`/usr/local/bin/virtualenvwrapper.sh`
在使用virtualenvwrapper时， 需要配置登录的shell初始化脚本， 将virtualenvwrapper.sh的信息读入当前的shell环境。这里以base为例， 通过对用户根目录下（即/home/[username]）的.bashrc配置文件进入如下修改即可。
修改.bashrc:

```
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
    export WORKON_HOME=/opt/env
    source /usr/local/bin/virtualenvwrapper.sh
fi
```

#####常用命令

创新的虚拟环境
- mkvirtualenv [env1]
该命令会帮我们创建一个新环境,默认情况下，环境的目录是.virtualenv/en1,创建过程中它会自动帮我们安装pip，以后我们要安装新依赖时可直接使用pip命令。
创建完之后，自动切换到该环境下工作，可看到提示符变为：
(env1)$
在这个环境下安装的依赖不会影响到其他的环境
- lssitepackages 显示该环境中所安装的包

切换环境
- workon [env]
随时使用“workon 环境名”可以进行环境切换，如果不带环境名参数，则显示当前使用的环境
- deactivate
在某个环境中使用，切换到系统的python环境

其他命令
- showvirtualenv [env] 显示指定环境的详情。
- rmvirtualenv [env] 移除指定的虚拟环境，移除的前提是当前没有在该环境中工作。如在该环境工作，先使用deactivate退出。
- cpvirtualenv [source] [dest] 复制一份虚拟环境。
- cdvirtualenv [subdir] 把当前工作目录设置为所在的环境目录。
- cdsitepackages [subdir] 把当前工作目录设置为所在环境的sitepackages路径。
- add2virtualenv [dir] [dir] 把指定的目录加入当前使用的环境的path中，这常使用于在多个project里面同时使用一个较大的库的情况。
- toggleglobalsitepackages -q 控制当前的环境是否使用全局的sitepackages目录。


说明
--------
上面内容均来自网上整理


