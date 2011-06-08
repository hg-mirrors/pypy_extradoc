import sys, time
from sqrt import sqrt, Fix16

try:
    import pypyjit
    pypyjit.set_param(trace_limit=20000)
except ImportError:
    pass

type1 = eval(sys.argv[1])
a = time.time()
sqrt(type1(123456), 100000000)
b = time.time()
name = 'sqrt(%s):' % sys.argv[1]
print '%12s  ' % name, b - a

    
