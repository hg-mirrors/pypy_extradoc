from noborder import NoBorderImagePadded, NoBorderImage
from sobel import sobel_magnitude
from time import time
import sys

sys.setcheckinterval(2**30)
try:
    import pypyjit
    pypyjit.set_param(trace_limit=200000)
except ImportError:
    pass

Image = eval(sys.argv[1])
n = 1000

sobel_magnitude(Image(n, n))

a = time()
for i in range(10):
    sobel_magnitude(Image(n, n))
b = time()
print 'sobel(%s):' % Image.__name__, b - a
