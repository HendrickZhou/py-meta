# v4
# use class decorator
# works ok 


from inspect import Parameter, Signature

def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)

def sig_deco(*names):
    def wrapper(cls):
        # NOTICE! cls here is Stock cls object
        cls.__signature__ = make_signature(names)
        return cls
    return wrapper
    


class Structure:
    __signature__ = Signature()
    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for field, val in bound.arguments.items():
            setattr(self, field, val)


@sig_deco("name", "shares", "price")
class Stock(Structure):
    pass

@sig_deco("hostname", "port")
class Address(Structure):
    pass
