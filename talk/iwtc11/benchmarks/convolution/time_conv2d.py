from convolution import conv3x3, Array2D
from array import array
import sys, time

try:
    import pypyjit
    pypyjit.set_param(trace_limit=200000)
except ImportError:
    pass

conv3x3(Array2D(1001, 1001), Array2D(3,3)) # Warmup

a = time.time()
for i in range(10):
    conv3x3(Array2D(1000000, 3), Array2D(3,3))
b = time.time()
print 'conv3x3(3):   ', b - a

a = time.time()
for i in range(10):
    conv3x3(Array2D(1000, 1000), Array2D(3,3))
b = time.time()
print 'conv3x3(1000):', b - a


