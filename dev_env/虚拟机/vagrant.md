# windows+vagrant+virtualbox

## 介绍vagrant

我们做web开发的时候经常要安装各种本地测试环境，比如apache,php,mysql,redis等等。出于个人使用习惯，可能我们还是比较习惯用windows。虽然说在windows下搭建各种开发环境是可行的，各大开发环境都有windows版本。然而在windows下配置有时候会显得繁琐，并且还会导致开发环境（windows）和生产环境（lunix）不一致。
能不能在windows下也像linux那样开发？也许你想到了，用虚拟机。用虚拟机装个linux系统就好了。装完linux系统就设置共享目录，设置网络端口映射，等等。好像也有那么点繁琐。
还有，假如我们是一个团队进行开发，那么每个人的电脑上都要装个虚拟机+ linux系统+各种运行环境。手动设置麻烦不说，大家的开发环境不太一致（可能你装了apcahe我装了nginx等），也是头疼。能不能把各种设置都自动化，并且保持整个团队的开发环境一致呢？
Vagrant就是为了解决这个问题而生的。它使用开源 VirtualBox 作为虚拟化支持，可以轻松的跨平台部署

## 下载
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com/downloads.html)
- [虚拟镜像](http://www.vagrantbox.es/):根据自己要使用的系统下载相应的镜像(比如precise-server-cloudimg-amd64-vagrant-disk1.box)

## 安装
下载好上面的软件包后，先安装VirtualBox,然后安装Vagrant。都是双击即可安装的，所以没什么好介绍。下面介绍下怎么把镜像导入:
- 先新建一个工作目录,比如我新建了```D:\vagrant\ubuntu```
- 进入目录,输入命令初始化:```vagrant init unbutu12```
- 把下载的镜像(这里是precise-server-cloudimg-amd64-vagrant-disk1.box)复制到当前目录,执行```vagrant box add unbutu12 precise-server-cloudimg-amd64-vagrant-disk1.box```
- 检查是否导入成功:```vagrant box list```:
```
D:\vagrant\ubuntu>vagrant box list
ubuntu12 (virtualbox, 0)
```

## 配置
打开目录下的```Vagrantfile```文件，这里介绍一下配置:

1. 端口映射
   ```config.vm.network :forwarded_port, guest: 80, host: 8080```
   把上面这句代码前面的#号去掉。它表示映射本机的8080端口到虚拟机的80端口

2. 如果需要自己自由的访问虚拟机，但是别人不需要访问虚拟机，可以使用private_network，并为虚拟机设置IP
   ```config.vm.network :private_network, ip: 192.168.33.10```

3. 目录映射
   ```config.vm.synced_folder "D:/vagrant/shared", "/vagrant_data"```
   如果启用上面的命令，表示把本机的```D:/vagrant/shared```目录共享到虚拟机里的```/vagrant_data```目录

## 启动
在当前目录执行```vagrant up```命令。
虚拟机启动之后则可以通过```vagrant ssh```联入虚拟机进行进一步的环境配置，或者软件安装相关的工作，在Windows系统下，并不能直接通过```vagrant ssh```连到虚拟机，需要使用 Putty、Xshell 等第三方工具进行连接:
- 连接地址```127.0.0.1```，端口```2222```
- 登录的帐号```root```的密码为```vagrant```

## 导出
在当前目录执行```vagrant package```,输出:
```
D:\vagrant\ubuntu>vagrant package
==> default: Attempting graceful shutdown of VM...
==> default: Clearing any previously set forwarded ports...
==> default: Exporting VM...
==> default: Compressing package to: D:/vagrant/ubuntu/package.box
```
可以看到在当前目录生成了```package.box```,之后新建虚拟机就可以使用这个box.如果事先在你的虚拟机里建立好了各种开发环境，那么你直接把这个box给你的团队其他成员安装，这样就可以省去一台台电脑部署的时间，还可以保持开发环境一致。很方便有木有


## 其他命令
下面列举出一些常用的cmd操作命令
- ```vagrant up```: 启动虚拟机
- ```vagrant halt```: 关闭虚拟机——对应就是关机
- ```vagrant suspend```: 暂停虚拟机——只是暂停，虚拟机内存等信息将以状态文件的方式保存在本地，可以执行恢复操作后继续使用
- ```vagrant resume```: 恢复虚拟机 —— 与前面的暂停相对应
- ```vagrant box remove ubuntu12```: 移除box，其中ubuntu12是box名
- ```vagrant destroy```: 删除虚拟机，删除后在当前虚拟机所做进行的除开Vagrantfile中的配置都不会保留

## 错误
启动时一直卡在这个界面:
```
D:\vagrant\ubuntu>vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
    default: Adapter 2: hostonly
==> default: Forwarding ports...
    default: 80 (guest) => 8080 (host) (adapter 1)
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
```
等了很久出现一个超时问题. 这时需要打开配置```Vagrantfile```文件打开下面配置:
```
config.vm.provider "virtualbox" do |vb|
  # Display the VirtualBox GUI when booting the machine
  vb.gui = true

  # Customize the amount of memory on the VM:
  vb.memory = "1024"
end
```
这样启动过程会出现界面，可以看到具体错误. 我这里是由于biso未开启```VT-x/AMD-V```支持.开启后保存重启即可.

## 附加
[启动多个虚拟机](http://www.thisprogrammingthing.com/2015/multiple-vagrant-vms-in-one-vagrantfile/)

## 参考
- [在windows下进行linux开发：利用Vagrant+virtualbox](http://blog.star7th.com/2015/06/1538.html)
