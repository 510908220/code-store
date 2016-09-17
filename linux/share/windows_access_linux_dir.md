# Samba软件实现共享Linux文件系统给Windows用户

## 安装

unbutu 使用如下命令安装:
```
apt-get install samba
```

安装完成后，修改配置文件，打开：/etc/samba/smb.conf，在文件末尾加上如下配置:
```
[root]
  comment = root
  path = / 
  create mask = 0755
  writeable = yes 
  browseable = yes
  valid users = root
```
这个配置的意思是，创建一个名为root的共享，将根文件目录“/”共享给用户。允许登录的用户名是root.

然后给samba系统添加root用户，使用如下命令:
```
smbpasswd -a root
```
按照提示设置root用户的密码

重新启动samba服务
```
service smbd restart
```

## 使用

在需要访问该Linux系统的Windows客户机上面，打开Windows的资源管理器，在地址栏输入```:\\ip```

会发现，提示有一个共享root，双击访问时，提示输入用户名和密码，输入此前配置的root用户和密码即可访问。这里就是Samba软件实现了CIFS的服务端，Windows资源管理作为客户端访问远程的共享文件系统。为了更为方便的使用该文件系统，还可以将该共享映射成一个本地的盘符，让Windows上面的各种工具像使用本地磁盘一样使用该目录。所有在Windows上面对该共享做的操作都会实时同步到Linux系统上面。


## 参考
- http://codefine.co/2451.html