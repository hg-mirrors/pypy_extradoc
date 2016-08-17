
class A(object):
    pass

def f():
    a = A()
    a.i = 2000000
    while a.i:
        a.i -= 1

f()
