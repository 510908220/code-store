#问题整理

## ssh-permissions-are-too-open-error
[ssh-permissions-are-too-open-error](http://stackoverflow.com/questions/9270734/ssh-permissions-are-too-open-error)
当私钥从linux拷贝到windows，再从windows拷贝到linux出现的.

## pip 安装的ansible没配置
从这里获取配置[getting-the-latest-configuration)](http://docs.ansible.com/ansible/intro_configuration.html#getting-the-latest-configuration)

## host check
```
The authenticity of host '192.168.33.102' can't be established.
The ssh-rsa key fingerprint is 3db8688a0c3eea61ac3bd2a6849e87cb.
Are you sure you want to continue connecting (yes/no)?
```
[how-to-ignore-ansible-ssh-authenticity-checking](http://stackoverflow.com/questions/32297456/how-to-ignore-ansible-ssh-authenticity-checking)

## 当密钥需要密码时
```
192.168.33.102 ansible_ssh_user=root  ansible_ssh_private_key_file=/root/id_rsa_db  ansible_ssh_pass=xxx
```

默认使用ssh链接会卡主. 换成```-c paramiko```可以。
