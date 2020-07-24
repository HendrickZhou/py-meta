# -*- coding: utf-8 -*-
# let's make it type checking

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

class Integer(Typed):
    ty = int

class String(Typed):
    ty = str

class Float(Typed):
    ty = float

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
    name = String("name")
    shares = Integer("shares")
    price = Float("price")

class Address(Structure):
    _fields = ["hostname", "port"]

