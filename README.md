# 项目开发规范
### 0 总体规范
--------------------
>绝大多数情况下，开发请遵守[PEP8 code style](https://www.python.org/dev/peps/pep-0008/)       

>严格按git工作流更新代码，git commit的信息格式严格规定为"名字-年月日-做了什么事"，例如
```git
git commit -m "李洋-20181213-更新README文档"
git commit -m "李洋-20181214-增加代码规范"
git commit -m "李洋-20181214-修复信号不能传递的bug"
git commit -m "李洋-20181215-删除旧版文档"
```
上面的信息由"动作（更新/增加/修复/删除/发布/回退等）+动作针对的对象"    

>信息优先保证简明扼要，请不要超过30个汉字，实在过长请在开发组群里面特别说明

>密钥类文件严禁增加至版本控制系统！最好增加至自己的操作系统的环境变量

>项目名称请勿更改

### 1 代码长度及缩进
--------------------
单行79个字符，除非函数的参数过多可以酌情超过，参数太多请折行
```python
from your_project.settings import appkey, appsecret, agent_id
from dingtalk_sdk_gmdzy2010.authority_request import AccessTokenRequest


# 下面的函数参数过多，超过79个字符的参数折行到下一行
def test(argument_1, argument_1, argument_1, argument_1, argument_1, argument_1,
         argument_1,):
    pass
```
代码缩进最好不要超过四层
```python
class MyClass:
    """Example doc"""
    
    # 第一层缩进
    def method_1(self, *args, **kwargs):
        foo = 1
        # 第二层缩进
        if foo > 1:
            # 第三层缩进
            print("test")
        return foo
    
    def method_2(self):
        pass
    
```
全局变量最好全部大写，模块内部的变量用小写加下划线，变量和赋值符之间前后分别有一个空格
```python
# local variable
foo_bar = 1

# global variable
FOO_BAR = 2
```

### 2 命名规范
--------------------
所有的命名`优先`保证语义化，看到对象名称就知道这个对象是用来做什么的
```python
class AccessToken:
    """test __doc__"""
    
    def get_access_token(self):
        pass
```

类名称用大骆驼命名规则，方法/属性名用单词加下划线，例如：
```python
class MyClass:
    """test __doc__"""
    
    def test_method(self):
        pass
        
```
私有属性/方法以单下划线开头，例如`_foo`，`_bar`，`_foo()`，关于私有属性请自行查资料了解
```python
class MyClass:
    """test __doc__"""
    # 类私有属性
    _question = None
    
    def __init__(self):
        # 实例私有属性
        self._private = None
    
    # 私有方法（类私有和实例私有方法与下面类似）
    def _test_method(self):
        pass
```

每块代码中间请两个空行隔开，从import语句到class，或者函数def
类的方法与方法之间用一个空行隔开
```python
from example_module import some_function


# 上面两个空行
def test():
    pass


# 上面两个空行
class MyClass:
    """Example doc"""
    
    # 实例方法与__doc__字符串之间用一个空行隔开
    def method_1(self, *args, **kwargs):
        pass
    
    # 同上注释
    def method_2(self):
        pass
```

### 3 开发风格
--------------------
>采用TDD模式，测试驱动开发，先写测试用例，再发布正式代码

>测试用pytest模块

### 4 代码合并
--------------------
提交时间：每天提交代码的时间大约为下班前1小时，请勿耽误审核人合并  

提交频次：请尽量保证每天提交一次有意义的更新，提高工作效率  

代码审核：李洋    

注：代码审核人将针对相关代码做标示，若再次更新未更改，审核人将直接重构，不再通知到当事人
```python
from example_module import some_function


# 这里的类描述文档很不清晰，请尽量增加详细说明，这个类是对哪种行为或者特征的封装
class MyClass:
    """Example doc"""
    
    # 请更换下列方法名称，建议名称XXX，更容易维护
    def method_1(self, *args, **kwargs):
        pass
```

### 5 CI/CD
--------------------
前期选择线上CI，CD视后期项目难度来选择    

对外发布频次为每周release一个版本，版本号采用点号隔开的3位（即：v主版本.子版本.孙版本
```
v0.0.1
v0.1.0
v1.0.2
```
具体而言，正式发布整个项目为主版本，增加一个Django app视为一个子版本，某个app内部功能更新为孙版本

### 6 项目分工
--------------------
>用户，微信/钉钉/顺丰接入，报告在线生成服务      

>技术支持，售后，实验

>商务，销售，财务，代理商
