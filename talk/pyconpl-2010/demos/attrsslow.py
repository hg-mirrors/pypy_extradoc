
class A(object):
    def __init__(self):
        self.d = {'a': 3, 'b': 4}
    
    def __getattr__(self, attr):
        return self.d[attr]

def f():
    a = A()
    i = 0
    while i < 1000000:
        a.a
        i += 1

f()
