from convolution import _conv3x3, Array2D, _dilate3x3, _erode3x3
from array import array
import sys, time

try:
    import pypyjit
    pypyjit.set_param(trace_limit=200000)
except ImportError:
    pass

# Warmup
_conv3x3(Array2D(1010, 1010), Array2D(3,3)) 
_dilate3x3(Array2D(1010, 1010), Array2D(3,3))

a = time.time()
for i in range(10):
    _conv3x3(Array2D(1000000, 3), Array2D(3,3))
b = time.time()
print 'conv3x3(3):   ', b - a

a = time.time()
for i in range(10):
    _conv3x3(Array2D(1000, 1000), Array2D(3,3))
b = time.time()
print 'conv3x3(1000):', b - a

a = time.time()
for i in range(10):
    _dilate3x3(Array2D(1000, 1000), Array2D(3,3))
b = time.time()
print 'dilate3x3(1000):', b - a
