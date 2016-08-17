
class X:
    def __init__(self, x):
        self.y = x

    def m(self):
        return self.y + 3

def two(x):
    return X(x).m()

def one(x):
    if x:
        return two(x)
    else:
        return 3
