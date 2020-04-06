# v2
# lose the help calling signature
# no checking
# can't do keyword arguments



class Structure:
    _fields = []
    def __init__(self, *args):
        # NOTICE! the self here is instance of Stock!
        # see pythontutor for more details
        for field, val in zip(self._fields, args):
            setattr(self, field, val)



class Stock(Structure):
    _fields = ["name", "shares", "price"]

class Address(Structure):
    _fields = ["hostname", "port"]
