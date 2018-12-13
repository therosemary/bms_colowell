# 项目开发规范
### 0 绝大多数情况下，开发请遵守[PEP8 code style](https://www.python.org/dev/peps/pep-0008/)
### 1 单行79个字符，除非函数的参数过多可以酌情超过，参数太多请折行
>单行79个字符，除非函数的参数过多可以酌情超过，参数太多请折行
>>
```python
from your_project.settings import appkey, appsecret, agent_id
from dingtalk_sdk_gmdzy2010.authority_request import AccessTokenRequest


# 下面的函数参数过多，将超过的参数折行到下一行
def test(argument_1, argument_1, argument_1, argument_1, argument_1, argument_1,
         argument_1,):
    pass

```
### 2 命名规范：
>类名称用大骆驼命名规则，方法/属性名用单词加下划线，`MyClass`，`test_method()`
>私有属性/方法以单下划线开头，例如`_foo`，`_bar`，`_foo()`，关于私有属性请自行查资料了解
>每块代码中间请两个空行隔开，从import语句到class，或者函数def
>类的方法与方法之间用一个空行隔开
```python
from your_project.settings import appkey, appsecret, agent_id
from dingtalk_sdk_gmdzy2010.authority_request import AccessTokenRequest


# 上面两个空行
def test():
    pass


class MyClass:
    """Example doc"""
    
    # 实例方法与__doc__字符串之间用一个空行隔开
    def method_1(self, *args, **kwargs):
        pass
    
    def method_2(self):
        pass
    
```
