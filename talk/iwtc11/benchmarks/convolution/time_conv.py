from convolution import conv3, conv5
from array import array
import sys, time

a = time.time()
conv3(array('d', [1]) * 100000000,
      array('d', [-1, 0, 1]))
b = time.time()
print 'conv3:        ', b - a

a = time.time()
conv5(array('d', [1]) * 100000000,
      array('d', [1, 4, 6, 4, 1]))
b = time.time()
print 'conv5:        ', b - a

