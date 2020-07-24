# -*- coding: utf-8 -*-
# dot operation
# use meta class

# 在前面实现初始化传值过程和创建attr过程绑定的基础上，使用descriptor对attr进行修饰

# 在旧实现中，实现绑定的关键步骤是__init__中的setattr，这一步实现了_field中的字符id和绑定
# 注意这里的绑定本质上是assignment，而不是store，见文档
# Called when an attribute assignment is attempted. 
# This is called instead of the normal mechanism 
# (i.e. store the value in the instance dictionary). 
# name is the attribute name, value is the value to be assigned to it.

# 这一步等同于 执行了这个语句: self.field = val
# 老代码中，field还没有定义，不过这是python，你细品
# 在这个例子中field已经定义过了，那就不是初始化了，而是assignment，直接触发了field（descriptor对象）的__set__

# 宏观上来讲，_field的作用是给我们自动绑定attr提供key

from inspect import Parameter, Signature

###########################################
# new thing here
class Descriptor(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, inst, cls):
        print("Get")
        return inst.__dict__[self.name]

    def __set__(self, inst, val):
        print("Set")
        inst.__dict__[self.name] = val

    def __delete__(self, inst):
        print("del")
        del inst.__dict__[self.name]



############################################
def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)


# get called each time a class is created
class StructMeta(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        signature = make_signature(clsobj._fields)
        setattr(clsobj, "__signature__", signature)
        return clsobj
    

class Structure(metaclass=StructMeta):
    _fields = []
    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for field, val in bound.arguments.items():
            setattr(self, field, val)

    def __repr__(self):
        cls_name = type(self).__name__
        args = ' ,'.join(repr(getattr(self, name)) for name in self._fields)
        return cls_name + '(' + args + ')'


class Stock(Structure):
    _fields = ["name", "shares", "price"]
    name = Descriptor("name")
    shares = Descriptor("shares")
    price = Descriptor("price")

class Address(Structure):
    _fields = ["hostname", "port"]

