
l = []

class A(object):
    def __del__(self):
        print "called"
        l.append(self)

a = A()
del a
import gc
gc.collect()
del l[0]
gc.collect()
