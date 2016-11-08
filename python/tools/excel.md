# Excel处理

> 经常会将数据保存为excel格式方便阅读或者从excel读取数据进行处理. 这里对一些excel操作进行整理, 在需要的时候拈来即用.

python有很多处理excel的包, 这里介绍一下[Tablib](http://docs.python-tablib.org/en/latest/),并对其进行封装方便进一步使用.



## Tablib

直接上例子:

```python
# -*- coding: utf-8 -*-

import tablib

data = tablib.Dataset(headers=[u'姓名', u'籍贯', u'年龄'], title=u"个人信息")
data.append((u'刘德华', u'中国', 50))
data.append_separator(u'--------------分割线----------------')
data.append((u'金智贤', u'韩国', 30))

with open("data.xls", "wb") as f:
    f.write(data.xls)

```

excel文件内容为:

![](1.png)

读取数据:

```python
# -*- coding: utf-8 -*-

import tablib

data = tablib.Dataset().load(open('data.xls', "rb").read(), "xls")
print data.headers  # 表头,也就是第一行
print data[u'年龄']  # 年龄这一列数据
for row in data:  # 遍历除头以外的行
    print row
```



是不是感觉很简单呢?

但是平时我们可能会创建多个工作表(sheet),是否也支持？那必须的.

看代码:

```python
# -*- coding: utf-8 -*-

import tablib

data1 = tablib.Dataset(headers=[u'姓名', u'籍贯', u'年龄'], title=u"个人信息")
data1.append((u'刘德华', u'中国', 50))
data1.append_separator(u'--------------分割线----------------')
data1.append((u'金智贤', u'韩国', 30))

data2 = tablib.Dataset(headers=[u'歌手', u'歌曲'], title=u"歌星信息")
data2.append((u'许嵩', u'断桥残雪'))
data2.append_separator(u'--------------分割线----------------')
data2.append((u'周杰伦', u'公公偏头痛'))

book = tablib.Databook((data1, data2))
with open("data.xls", "wb") as f:
    f.write(book.xls)

```

执行结果:

![](2.png)

读取数据:

```python
# -*- coding: utf-8 -*-

import tablib

datas = tablib.Databook().load("xls", open('data.xls', "rb").read())
print len(datas.sheets())  # sheet个数
data = datas.sheets()[1]  # 选取第二个sheet

print data.headers  # 表头,也就是第一行
print data[u'歌曲']  # 年龄这一列数据
for row in data:  # 遍历除头以外的行
    print row

```



是不是感觉到操作excel特别简单呢.

这里只是演示的写excel，去excel也是特别简单.

## 封装操作

##### 写操作

```python
# -*- coding: utf-8 -*-

import tablib


class ExcelWriter(object):
    """
    Excel写,支持多sheet,例子:
    ex = ExcelWriter("test.xls")
    ex.add_data("演员列表", ["姓名"], [["周星驰"], ["周润发"]])
    ex.add_data("影视列表", ["影视", "演员"], [["上海滩", "周润发"], ["大话西游", "周星驰"]])
    ex.save()

    """
    
    def __init__(self, xls_file):
        self.datas = []
        self.xls_file = xls_file
    
    def add_data(self, title, headers, rows):
        data = tablib.Dataset(title=title)
        data.headers = headers
        for row in rows:
            data.append(row)
        self.datas.append(data)
    
    def save(self):
        book = tablib.Databook(self.datas)
        with open(self.xls_file, 'wb') as f:
            f.write(book.xls)
            
```

##### 读操作

```python
class ExcelReader(object):
    """
    reader = ExcelReader("test.xls")
    print reader[1].headers
    for row in reader[1]:
        print row
    """
    
    def __init__(self, xls_file):
        self.xls_file = xls_file
        self.sheets = []
        self.__load_data()
    
    def __load_data(self):
        datas = tablib.Databook().load("xls", open(self.xls_file, "rb").read())
        self.sheets = datas.sheets()
    
    def __getitem__(self, index):
        assert index < len(self.sheets)
        return self.sheets[index]
    
    @property
    def sheet_count(self):
        return len(self.sheets)

```

