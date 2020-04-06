# v3
# support kw and positional 
# provide signature
# check the param validity 
# rather annoying tho

from inspect import Parameter, Signature

def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)

class Structure:
    __signature__ = Signature()
    #__signature__ = make_signature([])
    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for field, val in bound.arguments.items():
            setattr(self, field, val)



class Stock(Structure):
    __signature__ = make_signature(["name", "shares", "price"])
class Address(Structure):
    __signature__ = make_signature(["hostname", "port"])
