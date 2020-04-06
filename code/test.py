class Meta(type):
    def __new__(cls, name, bases, clsdict):
        print("create customed cls object")
        return super().__new__(cls, name, bases, clsdict)

class Inter(metaclass = Meta):
    pass

class Spam(Inter):
    def __init__(self):
        print("instance created")

class Foo(Inter):
    def __init__(self):
        pass

s = Spam()
f= Foo()
