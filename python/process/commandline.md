# 进程命令行


## windows进程命令行获取

来源:[determining-running-programs-in-python](http://stackoverflow.com/questions/3429250/determining-running-programs-in-python)
```
import subprocess
cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
for line in proc.stdout:
    print line
```
