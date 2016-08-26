# pylint

pylint是一个python代码风格检查工具, 有很多特性.

- 代码风格(Coding Standard): 使用pep8作为代码风格标准,你如行的长度、变量是否使用等
- 错误检查(Error detection): 检查模块是否导入、接口是否实现等
- 重构帮助(Refactoring help): 可以检查重复的代码.
- 可定制化(Fully customizable): pylint有个默认的配置, 可以修改配置。 比如可以修改行限制长度、屏蔽掉不是那么重要的警告等.
- 编辑器集成(Editor integration): 可以集成到emacs、vim等
- IDE集成(IDE integration): 可以集成到像SPyder、Eclipse等IDE里.
- 持续集成(Continuous integration):可以很容易的和jenkins集成进来，持续改进代码，这个特性很nice. 

更详细的介绍可以看看官网[pylint](https://www.pylint.org/).

# 使用

#####生成配置文件
```pylint --generate-rcfile > pylint.cfg```
#####部分配置说明

- init-hook: 默认检查代码只能识别标准库以及安装的包, 自己项目里的包是识别不了的，其实主要就是不在``` sys.path```下. 通过这个配置项可以达到目的.
- disable: 屏蔽一些警告, 这里面的错误就不会提示了.
- output-format: 检查检查结果的格式, 默认是text， 如果使用jenkins时，需要修改为```parseable```否则jenkins插件解析不了.
- load-plugins: 插件,比如在检查django代码是可以添加[pylint-django](https://github.com/landscapeio/pylint-django) 这个插件.

#####检查
配置项可以写在命令行也可以使用配置文件里的.
```
pylint --load-plugins pylint_django --rcfile=pylint.cfg ${WORKSPACE} > pylint.xml
```


