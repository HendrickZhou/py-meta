# -*- coding: utf-8 -*-
# 多重继承加强版

# 在上一个基础上又增加了一个Regex类的继承
# 这里多了一个trick，使用**kwargs来连续传递参数给嵌套的函数
# 由上一个知道Regex,Sized的__init__的调用形成了一个链路
# 使用这种形式，可以将kwargs连续传递下去，每个调用的函数只会pull out自己需要的kwarg
# def f1(*args, specific_kw_arg, **kwargs):
#   do something with specific_kwa_arg
#   f2(*args, **kwargs)



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

class Typed(Descriptor):
    ty = None # expected type

    def __set__(self, inst, val):
        if not isinstance(val, self.ty):
            raise TypeError("Expect:{}".format(self.ty))
        super().__set__(inst, val)

class Positive(Descriptor):
    def __set__(self, inst, val):
        if val <= 0:
            raise ValueError("Expect positive value")
        super().__set__(inst, val)

class Sized(Descriptor):
    def __init__(self, *args, max_len, **kwargs):
        self.max_len = max_len
        super().__init__(*args, **kwargs)

    def __set__(self, inst, val):
        if len(val) > self.max_len:
            raise ValueError("Length limit exceeded")
        super().__set__(inst, val)



class Integer(Typed):
    ty = int

class String(Typed):
    ty = str

class Float(Typed):
    ty = float

class IntegerPositive(Integer, Positive):
    pass

# class StringSized(String, Sized):
#     pass


import re
class Regex(Descriptor):
    def __init__(self, *args, pat, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    def __set__(self, inst, val):
        if not self.pat.match(val):
            raise ValueError("Invalid pattern")
        super().__set__(inst, val)

class StringSizedRegex(String, Sized, Regex):
    pass

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
    name = StringSizedRegex("name", pat = "[A-Z]", max_len = 5)
    shares = IntegerPositive("shares")
    price = Float("price")

s = Stock("ABCDE", 100, 0.1)

