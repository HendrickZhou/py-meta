from functools import wraps, partial

def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__qualname__)
        return func(*args, **kwargs)
    return wrapper

def debug_v(func):
    print(func.__name__)
    return func


# basically just patch
def debugmethods(cls):
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val))

    return cls

# basically just patch 
def debugattr(cls): 
    orig_getattribute__ = cls.__getattribute__

    def __getattribute__(self, name):
        print('Get:', name)
        return orig_getattribute__(self, name)
    cls.__getattribute__ = __getattribute__

    return cls
