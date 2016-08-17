from carbonpython import export
import time

@export(int)
def fn(N):
    t1 = time.clock()
    z = 0
    for index in xrange(N):
        x = 2.34+index
        y = 3.45+index
        z = (x*x)+(y*y)+index
    t2 = time.clock()
    print t2-t1, 'seconds'
    return z
