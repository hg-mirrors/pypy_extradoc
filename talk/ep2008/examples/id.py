
class A(object):
    pass

x = [A() for i in range(1000000)]
y = [id(i) for i in x]
