# v5
# use meta class

from inspect import Parameter, Signature

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

class Address(Structure):
    _fields = ["hostname", "port"]

