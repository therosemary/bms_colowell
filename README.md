# 项目开发规范
### 0 总体规范
绝大多数情况下，开发请遵守[PEP8 code style](https://www.python.org/dev/peps/pep-0008/)

### 1 代码长度及缩进
单行79个字符，除非函数的参数过多可以酌情超过，参数太多请折行
```python
from your_project.settings import appkey, appsecret, agent_id
from dingtalk_sdk_gmdzy2010.authority_request import AccessTokenRequest


# 下面的函数参数过多，超过79个字符的参数折行到下一行
def test(argument_1, argument_1, argument_1, argument_1, argument_1, argument_1,
         argument_1,):
    pass

```
缩进最好不要超过四层
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

### 2 命名规范：
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
