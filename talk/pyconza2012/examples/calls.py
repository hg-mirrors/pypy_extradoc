
import sys, time

def inner(a, b, c):
    pass

def simple_call(a, b, c):
    inner(a, b, c)

def simple_call2(a, b, c):
    inner(a, c=c, b=b)

def star_call(a, b, c):
    inner(*(a, b, c))

def star_call_complex(a, b, c):
    inner(*(a, b), **{'c': c})

def abomination(a, b, c):
    inner(**locals())

def run(func):
    count = int(sys.argv[1])
    t0 = time.time()
    for i in range(count):
        func(i, i, i)
    tk = time.time()
    t = (tk - t0) / count
    print "%.2e per call, %d cycles" % (t, int(t * 1.7e9))

for f in [simple_call, simple_call2, star_call, star_call_complex, abomination]:
    run(f)
