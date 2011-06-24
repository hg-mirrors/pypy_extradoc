from array import array
from math import log10, sqrt

def _conv3(a, k, n=1):
    assert len(k)==3
    b = array(a.typecode, [0]) * (len(a) - 2)
    while n:
        n -= 1
        for i in xrange(len(b)):
            b[i] = k[2]*a[i] + k[1]*a[i+1] + k[0]*a[i+2]
    return b

def conv3(args):
    n = int(args[0])
    _conv3(array('d', [1]) * (100000000/n),
           array('d', [-1, 0, 1]), n)
    return 'conv3(array(1e%d))' % log10(100000000/n)

def _conv5(a, k, n=1):
    assert len(k)==5
    b = array(a.typecode, [0]) * (len(a) - 4)
    while n:
        n -= 1
        for i in xrange(len(b)):
            b[i] = k[4]*a[i] + k[3]*a[i+1] + k[2]*a[i+2] + k[1]*a[i+3] + k[0]*a[i+4]
    return b

def conv5(args):
    n = int(args[0])
    _conv5(array('d', [1]) * (100000000/n),
           array('d', [1, 4, 6, 4, 1]), n)
    return 'conv5(array(1e%d))' % log10(100000000/n)

class Array2D(object):
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.data = array('d', [0]) * (w*h)

    def _idx(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return y*self.width + x
        raise IndexError

    def __getitem__(self, (x, y)):
        return self.data[self._idx(x, y)]

    def __setitem__(self, (x, y), val):
        self.data[self._idx(x, y)] = val

    def __cmp__(self, other):
        return cmp(self.data, other.data)

    def setup(self, data):
        for y in xrange(self.height):
            for x in xrange(self.width):
                self[x, y] = data[y][x]
        return self

def _conv3x3(a, b, k):
    assert k.width == k.height == 3
    for y in xrange(1, a.height-1):
        for x in xrange(1, a.width-1):
            b[x, y] = k[2,2]*a[x-1, y-1] + k[1,2]*a[x, y-1] + k[0,2]*a[x+1, y-1] + \
                      k[2,1]*a[x-1, y]   + k[1,1]*a[x, y]   + k[0,1]*a[x+1, y]   + \
                      k[2,0]*a[x-1, y+1] + k[1,0]*a[x, y+1] + k[0,0]*a[x+1, y+1]
    return b

def morphology3x3(a, b, k, func):
    assert k.width == k.height == 3
    for y in xrange(1, a.height-1):
        for x in xrange(1, a.width-1):
            b[x, y] = func(k[2,2]*a[x-1, y-1], k[1,2]*a[x, y-1], k[0,2]*a[x+1, y-1], \
                           k[2,1]*a[x-1, y]  , k[1,1]*a[x, y]  , k[0,1]*a[x+1, y]  , \
                           k[2,0]*a[x-1, y+1], k[1,0]*a[x, y+1], k[0,0]*a[x+1, y+1])
    return b

def _dilate3x3(a, b, k):
    return morphology3x3(a, b, k, max)

def _erode3x3(a, k):
    return morphology3x3(a, k, min)

def conv3x3(args):
    a = Array2D(int(args[0]), int(args[1]))
    b = Array2D(a.width, a.height)
    for i in range(10):
        _conv3x3(a, b, Array2D(3,3))
    return 'conv3x3(Array2D(%sx%s))' % tuple(args)

def dilate3x3(args):
    a = Array2D(int(args[0]), int(args[1]))
    b = Array2D(a.width, a.height)
    for i in range(10):
        _dilate3x3(a, b, Array2D(3,3))
    return 'dilate3x3(Array2D(%sx%s))' % tuple(args)

def _sobel_magnitude(a):
    b = Array2D(a.width, a.height)    
    for y in xrange(1, a.height-1):
        for x in xrange(1, a.width-1):
            dx = -1.0 * a[x-1, y-1] + 1.0 * a[x+1, y-1] + \
                 -2.0 * a[x-1, y]   + 2.0 * a[x+1, y] + \
                 -1.0 * a[x-1, y+1] + 1.0 * a[x+1, y+1]
            dy = -1.0 * a[x-1, y-1] -2.0 * a[x, y-1] -1.0 * a[x+1, y-1] + \
                  1.0 * a[x-1, y+1] +2.0 * a[x, y+1] +1.0 * a[x+1, y+1]
            b[x, y] = sqrt(dx*dx + dy*dy) / 4.0
    return b

def sobel_magnitude(args):
    for i in range(10):
        _sobel_magnitude(Array2D(int(args[0]), int(args[1])))
    return 'sobel(Array2D(%sx%s))' % tuple(args)
