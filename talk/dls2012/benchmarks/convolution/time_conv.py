from convolution import conv3, conv5
from array import array
import sys, time
from math import log10

n = int(sys.argv[1])

a = time.time()
conv3(array('d', [1]) * (100000000/n),
      array('d', [-1, 0, 1]), n)
b = time.time()
print 'conv3(1e%d):   ' % log10(100000000/n), b - a

a = time.time()
conv5(array('d', [1]) * (100000000/n),
      array('d', [1, 4, 6, 4, 1]), n)
b = time.time()
print 'conv5(1e%d):   ' % log10(100000000/n), b - a

