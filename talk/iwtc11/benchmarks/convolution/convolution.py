from array import array

def conv3(a, k, n=1):
    assert len(k)==3
    b = array(a.typecode, [0]) * (len(a) - 2)
    while n:
        n -= 1
        for i in xrange(len(b)):
            b[i] = k[2]*a[i] + k[1]*a[i+1] + k[0]*a[i+2]
    return b

def conv5(a, k, n=1):
    assert len(k)==5
    b = array(a.typecode, [0]) * (len(a) - 4)
    while n:
        n -= 1
        for i in xrange(len(b)):
            b[i] = k[4]*a[i] + k[3]*a[i+1] + k[2]*a[i+2] + k[1]*a[i+3] + k[0]*a[i+4]
    return b

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

def conv3x3(a, k):
    assert k.width == k.height == 3
    b = Array2D(a.width, a.height)
    for y in xrange(1, a.height-1):
        for x in xrange(1, a.width-1):
            b[x, y] = k[2,2]*a[x-1, y-1] + k[1,2]*a[x, y-1] + k[0,2]*a[x+1, y-1] + \
                      k[2,1]*a[x-1, y]   + k[1,1]*a[x, y]   + k[0,1]*a[x+1, y]   + \
                      k[2,0]*a[x-1, y+1] + k[1,0]*a[x, y+1] + k[0,0]*a[x+1, y+1]
    return b
