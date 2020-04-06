from debugly import *

@debug
def add(x, y):
    return x+y

@debug_v
def sub(x,y):
    return x-y


#@debugmethods
#@debugattr
class Spam:
    def a(self):
         pass

    def b(self):
        pass
