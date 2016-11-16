# paramiko 使用整理

##FAQ

问题一:paramiko.SSHException: Unknown server xx.xx.xx.xxx
原因:
解决:
```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('127.0.0.1', username=username, password=password)
stdin, stdout, stderr = client.exec_command('ls -l')
```


## 参考
- [ssh_remote_login](http://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html)
