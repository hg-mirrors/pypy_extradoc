
import sys, time

def inner(a, b, c):
    pass

def simple_call(a, b, c):
    inner(a, b, c)

def simple_call2(a, b, c):
    inner(a, c=c, b=b)

def simple_method(a, b, c):
    c.m(a, b)

def star_call(a, b, c):
    inner(*(a, b, c))

def star_call_complex(a, b, c):
    inner(*(a, b), **{'c': c})

def abomination(a, b, c):
    inner(**locals())

class A(object):
    def m(self, a, b):
        pass

def run(func):
    count = int(sys.argv[1])
    t0 = time.time()
    o = A()
    for i in xrange(count):
        func(i, i, o)
    tk = time.time()
    t = (tk - t0) / count
    print "%s %.2e per call, %d cycles" % (func.func_name, t, int(t * 1.7e9))

for f in [simple_call, simple_call2, simple_method, star_call, star_call_complex, abomination]:
    run(f)

