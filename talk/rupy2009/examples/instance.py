
class A(object):
    def __init__(self, next, v):
        self.next = next
        self.v    = v

def f():
    a = A(None, 0)
    i = 0
    while i < 1000000:
        a = A(a, i)
        i += 1
    return a

f()
