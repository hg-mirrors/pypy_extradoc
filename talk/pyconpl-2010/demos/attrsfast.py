
class A(object):
    def __init__(self):
        self.a = 3
        self.b = 4

def f():
    a = A()
    i = 0
    while i < 1000000:
        a.a
        i += 1

f()

