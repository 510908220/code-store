# 文件压缩与解压(7z)

> 平时需要在多台机器传输一些大的文件,为了更快的传输,需要对文件尽可能的压缩. ```7z```是使用较多的压缩软件(拥有极高的压缩比),这里简单整理一下```7z```的使用,方便日后查看.

## 安装

```shell
 apt-get install p7zip-full
```

## 使用

​	 先看一下7z的命令格式:

```bash
Usage: 7z <command> [<switches>...] <archive_name> [<file_names>...]
       [<@listfiles...>]

<Commands>
  a: Add files to archive
  b: Benchmark
  d: Delete files from archive
  e: Extract files from archive (without using directory names)
  l: List contents of archive
  t: Test integrity of archive
  u: Update files to archive
  x: eXtract files with full paths
<Switches>
  -ai[r[-|0]]{@listfile|!wildcard}: Include archives
  -ax[r[-|0]]{@listfile|!wildcard}: eXclude archives
  -bd: Disable percentage indicator
  -i[r[-|0]]{@listfile|!wildcard}: Include filenames
  -m{Parameters}: set compression Method
  -o{Directory}: set Output directory
  -p{Password}: set Password
  -r[-|0]: Recurse subdirectories
  -scs{UTF-8 | WIN | DOS}: set charset for list files
  -sfx[{name}]: Create SFX archive
  -si[{name}]: read data from stdin
  -slt: show technical information for l (List) command
  -so: write data to stdout
  -ssc[-]: set sensitive case mode
  -t{Type}: Set type of archive
  -u[-][p#][q#][r#][x#][y#][z#][!newArchiveName]: Update options
  -v{Size}[b|k|m|g]: Create volumes
  -w[{path}]: assign Work directory. Empty path means a temporary directory
  -x[r[-|0]]]{@listfile|!wildcard}: eXclude filenames
  -y: assume Yes on all queries
```

​	熟悉一下命令使用有助于后面的理解. 下面的例子都是基于这样的目录结构的:

```bash
root@iZ25r4jcgl5Z:~/test# tree -a shop/
shop/
├── config
├── fruits
│   ├── apple
│   └── orange
└── .svn
    ├── pristine
    │   └── 00.txt
    ├── tmp
    └── wc.db

4 directories, 5 files
```

#### 例子1:压缩文件

```
7z a archive.7z /root/test/shop
```

​	输出:

```
Creating archive archive.7z

Compressing  shop/fruits/apple      
Compressing  shop/config      
Compressing  shop/fruits/orange      
Compressing  shop/.svn/pristine/00.txt      
Compressing  shop/.svn/wc.db      

Everything is Ok
```

​	另外可以通过选项```-m```指定压缩级别,这里指定压缩最高的方式```-mx9```

```
7z a archive.7z /root/test/shop -mx9
```

#### 例子2:过滤特定目录

​	比如我像对svn目录进行打包,但是里面有一个隐藏目录.svn. 怎么去掉呢

```
7z  a archive.7z  /root/test/shop   -xr\!.svn
```

​	输出:

```
Creating archive archive.7z

Compressing  shop/fruits/apple      
Compressing  shop/config      
Compressing  shop/fruits/orange      

Everything is Ok
```

​	```-xr\!.svn```表示跳过.svn目录,其中r表示递归. 注意在控制台执行时需要转义```!```

#### 例子3:解压

```
7z x archive.7z -o/root/test/xx
```

​	查看xx目录可以看到多了一个shop目录.

```bash
root@iZ25r4jcgl5Z:~/test# ls xx/
shop
```

​	当在执行一遍解压命令会出现这个界面:

```bash
Processing archive: archive.7z

file /root/test/xx/shop/fruits/apple
already exists. Overwrite with 
shop/fruits/apple?
(Y)es / (N)o / (A)lways / (S)kip all / A(u)to rename all / (Q)uit? 
```

​	这个是覆盖文件提示,怎么避免呢,添加```-y```选项即可:

```bash
7z x archive.7z -o/root/test/xx -y
```

​	

## python封装

```
# -*- encoding: utf8 -*-
import os
import subprocess

"""
对7z命令的简单包装,方便使用
"""


def archive(dest_dir, archive_file, filters=[], level="-mx9", create_always=True):
    """
    dest_dir: 待压缩的目录
    archive_file:输出的压缩文件
    level:压缩级别
    filters: 过滤的目录列表
    create_always:每次都创建新的压缩文件
    """
    if create_always and os.path.exists(archive_file):
        os.remove(archive_file)
    
    cmd = "7z a {archive_file} {dest_dir} {level} {filter_str}".format(
        dest_dir=dest_dir,
        archive_file=archive_file,
        level=level,
        filter_str=" ".join(["-xr\!" + f for f in filters])
    )
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode == 0, err, cmd


def extract(archive_file, dest_dir):
    """
    archive_file:待解压的压缩文件
    dest_dir: 压缩文件解压到的目录
    """
    cmd = "7z x {archive_file} -o{dest_dir} -y".format(
        dest_dir=dest_dir,
        archive_file=archive_file,
    )
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode == 0, err, cmd

```



## 压缩级别
- -mx0: Don't compress at all.This is called "copy mode."
- -mx1: Low compression.This is called "fastest" mode.
- -mx3: Fast compression mode. Will automatically set various parameters.
- -mx5: Same as above, but "normal."
- -mx7: This means "maximum" compression.
- -mx9: This means "ultra" compression.You probably want to use this.


## 参考

- [7-zip-examples](https://www.dotnetperls.com/7-zip-examples)
- [7zip-command-line-exclude-folders-by-wildcard-pattern](https://superuser.com/questions/97342/7zip-command-line-exclude-folders-by-wildcard-pattern)