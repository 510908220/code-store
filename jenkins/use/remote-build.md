# Jenkins远程构建


为了方便自动化构建，可以通过url触发构建.这里暂时不考虑需要登陆的情况.

## 不带参数的构建


- 设置token:构建触发器–>触发远程构建–>身份验证令牌

- 发送一个get请求:`http://localhost:8080/job/job_name/build?token=xxxxx`

## 带参数构建

由于构建的版本号参数是通过url动态传入的。所以构建方式是选择为```buildWithParameters```

- 设置token:构建触发器-->触发远程构建-->身份验证令牌
- 将构建改为"Build with Parameters"(默认是"立即构建")：
	- 安装插件[Dynamic Parameter Plug-in](https://wiki.jenkins-ci.org/display/JENKINS/Dynamic+Parameter+Plug-in)
	- 设置参数构建:参数化构建过程-->添加参数,这样就可以通过url传入参数了,这里我创建了一个`revision`参数如图:
![](http://ocidwvtj2.bkt.clouddn.com/jenkins_build_with_parameters.png)
- 点击```Build with Parameters```,输入构建参数，如图:
![](http://ocidwvtj2.bkt.clouddn.com/enter_build_with_parameters.png),点击开始构建

  上面是手动触发`带参数的构建`方式,通过url的话类似这样:
http://localhost:8080/job/job_name/buildWithParameters?token=xxx&revision=13833
