
class A(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

def obj_good():
    a = A(1, 2, 3)
    s = 0
    for i in range(SIZE):
        s += getattr(a, 'a') + a.b + a.c
    return s

def obj_bad():
    a = A(1, 2, 3)
    s = 0
    for i in range(SIZE):
        a.__dict__[i] = i
        s += a.__dict__[i]
    return s

def dict_bad():
    a = {'a': 1, 'b': 2, 'c': 3}
    s = 0
    for i in range(SIZE):
        s += a['a'] + a['b'] + a['c']
    return s

def dict_good():
    a = {}
    s = 0
    for i in range(SIZE):
        a[i] = i
        s += a[i]
    return s

import timeit
SIZE = 10000

print "obj, few", timeit.timeit(obj_good, number=SIZE)
print "obj, many", timeit.timeit(obj_bad, number=SIZE)
print "dict, many", timeit.timeit(dict_good, number=SIZE)
print "dict, few", timeit.timeit(dict_bad, number=SIZE)
