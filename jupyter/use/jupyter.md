# Jupyter

[jupyter](http://jupyter.org/)简单点看就是一个web程序. 有如下特性:

- 多语言:支持40多个语言
- 易于分享:可以通过email、github、[Jupyter Notebook Viewer](http://nbviewer.jupyter.org/)等进行分享.
- 交互式控件:代码可以产生丰富的输出像图片、视频、LaTeX、JavaScript. 
- 大数据整合: 探索相同数据在pandas、scikit-learn, ggplot2, dplyr等中的效果.


## IPython 和 Notebooks 如何工作
其实IPython和Notebooks的关系简单描述就是Jupyter是一个web程序,在执行python代码时会调用ipython Kernel去解释.

#####The IPython Kernel

IPython Kernel是一个单独的进程,负责运行用户的代码. 前端像notebook 或者Qt console是通过一些json消息进行交互. IPython Kernel和  terminal IPython核心的执行部分是共享的，如图:
![](http://jupyter.readthedocs.io/en/latest/_images/ipy_kernel_and_terminal.png)

##### Notebooks
先看一下架构图
![](http://jupyter.readthedocs.io/en/latest/_images/notebook_components.png)

可以看到实际我们使用jupyter时都是与Notebook server的交互, 只有在执行代码时才会去调用Ipython Kernel, 所以如果不运行代码，没有Kernel可以正常使用jupyter.

## 命令讲解

当安装完成后，在控制台输入```jupyter notebook -h```会显示常用的命令,这里介绍一些基本的:
```
(jupyter) root@iZ25r4jcgl5Z:~# jupyter notebook  --h
usage: jupyter-notebook [-h] [--certfile NOTEBOOKAPP.CERTFILE]
                        [--ip NOTEBOOKAPP.IP] [--pylab [NOTEBOOKAPP.PYLAB]]
                        [--log-level NOTEBOOKAPP.LOG_LEVEL]
                        [--port-retries NOTEBOOKAPP.PORT_RETRIES]
                        [--notebook-dir NOTEBOOKAPP.NOTEBOOK_DIR]
                        [--client-ca NOTEBOOKAPP.CLIENT_CA]
                        [--config NOTEBOOKAPP.CONFIG_FILE]
                        [--keyfile NOTEBOOKAPP.KEYFILE]
                        [--port NOTEBOOKAPP.PORT]
                        [--transport KERNELMANAGER.TRANSPORT]
                        [--browser NOTEBOOKAPP.BROWSER] [--script] [-y]
                        [--no-browser] [--debug] [--no-mathjax] [--no-script]
                        [--generate-config]

```

可以通过 ```jupyter notebook --generate-config```生成默认的配置文(~/.jupyter/jupyter_notebook_config.py), 实际配置文件里的命令选项使用```jupyter notebook --help-all```可以看到，还是觉得配置文件里配置方便点. 下面简单修改一下配置文件.

##### 授权相关

- 启动登录和登出

```
# The login handler class to use.
c.NotebookApp.login_handler_class = 'notebook.auth.login.LoginHandler'

# The logout handler class to use.
c.NotebookApp.logout_handler_class = 'notebook.auth.logout.LogoutHandler'
```
</br>
- 设置密码

```
# Hashed password to use for web authentication.
# 
# To generate, type in a python/IPython shell:
# 
#   from notebook.auth import passwd; passwd()
# 
# The string should be of the form type:salt:hashed-password.
c.NotebookApp.password = 'sha1:e7d751dd20a4:4065717ff6d0aa3e05fb4b2fd997df7f588a392d'

```
密码的设置方式为(实际设置的密码是123456):
```
In [1]: from notebook.auth import passwd; passwd()
Enter password: 
Verify password: 
Out[1]: 'sha1:e7d751dd20a4:4065717ff6d0aa3e05fb4b2fd997df7f588a392d'
```
- 登录页面 

打开notebook可以看到如下登录页面:
![](http://ocidwvtj2.bkt.clouddn.com/jupyter_login.png)


##### 目录设置
```
# The directory to use for notebooks and kernels.
 c.NotebookApp.notebook_dir = u'/opt/notebooks'
```
这样所有的ipynb就会保存到指定目录下.
