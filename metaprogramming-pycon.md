## 1.fundamental

* `*args`: arguments by position,  `**kwargs` : arguments by keyword
  * `func（1，2，x = 3,  y = 4)`， `args = (1,2)`, `kwargs = {'x': 3, 'y' : 4}`
  * 可以直接使用tuple作为`*args`, dict作为`**kwargs`传入参数 
  * `(arg1, arg2, *, arg3, arg4)`  `*`后面的只能用keyword参数传进去
* class相关
  * `@classmethod`只能用在class level的method
  * `@staticmethod`一个被放在了class内部的method

* print is the one and only debugging method

## 2.Decorator

* 由于使用decorator会损失一些函数本身的信息，可以使用`functools`模块来处理

* args
  * `@decorator(args)`的实现代码中，最外层函数可以理解为为内层的函数**创造了一个环境** ，即给内层代码提供了一些可用的参数（`args`），而内部就是正常方式写的decorator wrapper
  * 如果觉得传入args会复杂化代码，还可以用`partial`和args postion hack

#### class decorator

此处涉及到的操作，如`__getattr__`等在data model中有详细介绍。

class访问attr时会“无条件”使用`__getattribute__`方法，因此这个方法可以作为class操作的入口

* 思路1：直接patch class对象的所有方法，一一加上decorator。
  * 访问方式，`vars(Cls)`or`Cls.__dict__`，作为字典
  * patch方式，`setattr`
* 思路2：直接patch class attribute访问入口

注意无论哪种方法都一定会涉及到一个中介。

#### 补充

decorator理解：

#### 1.function decorator

```python
@deco
def foo()
	pass

# 等价于
foo = deco(foo)
```

第一个点要注意的是，这是一个执行语句，不是一个定义语句！此时deco的函数已经被执行了。

仔细想想这个逻辑，deco这个func object(which contains code object)实际上是一个one-shot过程，只在@定义处执行过一次，而最后foo指向的，也一定不是其原本的code object

deco的定义语句的唯一作用，就要把foo指向的内容安排好，也就是用一个包含了原foo code object的wrapper，让其作为中间人来托管一切。

![deco](.\static\deco.png)

foo的每次执行，都是通过所指向的wrapper函数以及其闭包来实现的。

这就是为什么不能天真地写这样的decorator

```python
# bad example
def deco(func):
    print(func.__name__)
    return func
```

#### 2.class decorator

decorator的执行顺序是：class Spam定义正常过 ->跑deco函数,篡改class定义中的内容->将结果cls返回给Spam这个__变量__->s = Spam()正常使用创建实例

```python
@deco
class Spam:
    pass

#等价于
Spam = deco(Spam)
```

#### 3.deco with args

```python
@deco(2)
def foo():
    pass
#
realdeco = deco(2)
foo = realdeco(foo)


@deco(2)
class Spam:
    pass
#
realdeco = deco(2)
Spam = realdeco(Spam)
```



## 3.Metaclass

#### class创建步骤conceptually

1. 定义和body分离
2. 使用定义式创建空`clsdict`
3. `exec(body, globals(), clsdict)`，populate先前的`clsdict`
4. 用__名字， base，clsdict__ 创建类。 `MyClass = type('MyClass', (Base,), clsdict)`

#### `__new__`和`__init__`

在data model文档中有详细介绍

* `__new__`：__创建实例/instance__
* `__init__`： __customize it__

在Meta相关话题中暂时可以不用考虑`__init__`

#### type class

Main takeaway:

* type class通过`__new__`创建自定义类(`MyClass`)的class object。

由此可见：

* 所有类都是`type`类的实例/instance！！

cpython中的type和python语言接口中的type class具体联系还不清楚，但是可以很明显地看到两者的行为是一致的。

#### 再来看class的创建

关键是最后一步。

最后一步其实是`type`通过`__new__`方法创建了`MyClass`类对象

那我只要把`type` patch成一个有`__new__`方法的类不就可以实现自定义type了

![type](.\static\type)

在class创建的时候有一个可选参数`metaclass`，默认就是`type`，将其换成自定义即可

```python
class MyType(type):
    def __new__(cls, name, bases, clsdict)：
    	# do your only customization here
        clsobj = super().__new__(cls,name, bases, clsdict)
        return clsobj

class Spam(metaclass = MyType):
    pass
```

最后一点：metaclass调用的顺序！见本段开头

简之是在class body被记录之后开始调用meta class

#### 补充（metaclass中的继承）

* class的继承行为

简单理解就是python几乎啥都没干，只提供了attribute look up机制

子类要么override/ patch了父类的interface/attribute, 要么自己没有，在父类提供的接口中查找。

```python
class Inter:
    pass

class Spam(Inter):
    def __init__(self):
        print("instance created")
   
class Foo(Inter):
    def __init__(self):
        pass
```

这段代码在内存中，就是三个class object分别单独被创建，但是Inter所有指向的funcobject/ vars, Spam, Foo都可以指向or查找到。

*　meta的继承性

所有派生类的metaclass属性都是同一个base的metaclass

也就是说每个class定义都会call一遍metaclass中的`__new__`方法



## 4.example

见code sig_v1 - sig_v5.py, 综合了decorator 和 metaclass

知识点：

* inspect lib
* signature trick

总结：

无论是decorator和metaclass在这个例子中，核心思想都是对cls object进行attribute patching的操作（metaclass也是对`super().__new__()`新创建出来的object进行操作）

## 5.property and descriptor

