
import sys, time

def f():
    l = [None]
    for i in range(int(sys.argv[1])):
        l[0] = (i,)

def g():
    m = int(sys.argv[1])
    l = [None] * m
    for i in range(m):
        l[i] = i

t0 = time.time()
f()
t1 = time.time()
g()
t2 = time.time()
print "long living", t2 - t1, "short living", t1 - t0
