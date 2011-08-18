from array import array
import math

try:
    import numpy
    import scipy.signal
except ImportError:
    pass
else:
    class NumpyImage(numpy.ndarray):
        def __new__(cls, a):
            return numpy.ndarray.__new__(cls, a.shape, a.dtype, a)
        @property
        def typecode(self):
            return self.dtype
        @property
        def width(self):
            return self.shape[1]
        @property
        def height(self):
            return self.shape[0]
    

class Image(array):
    def __new__(cls, w, h, typecode='d', fromfile=None):
        self = array.__new__(cls, typecode)
        return self
        
    def __init__(self, w, h, typecode='d', fromfile=None):
        self.width = w
        self.height = h
        if fromfile is not None:
            self.fromfile(fromfile, w * h)
        else:
            self.append(0)
            self *= w*h

    def new(self):
        return Image(self.width, self.height, self.typecode)
            
    def _idx(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return y*self.width + x
        raise IndexError

    def __getitem__(self, (x, y)):
        return array.__getitem__(self, self._idx(x, y))

    def __setitem__(self, (x, y), val):
        array.__setitem__(self, self._idx(x, y), val)

    def pixels(self, border=0):
        for y in xrange(border, self.height-border):
            for x in xrange(border, self.width-border):
                yield x, y

    def ndarray(self):
        return numpy.ndarray((self.height, self.width), self.typecode, self)

class ZeroPaddedImage(Image):
    def __getitem__(self, (x, y)):
        try:
            return array.__getitem__(self, self._idx(x, y))
        except IndexError:
            return 0

def wrap_numpy(fn):
    def f(a):
        return NumpyImage(fn(a.ndarray()))
    return f
    
def sobel_magnitude(a):
    b = a.new()
    for x, y in a.pixels(border=1):
        dx = -1.0 * a[x-1, y-1] + 1.0 * a[x+1, y-1] + \
             -2.0 * a[x-1, y]   + 2.0 * a[x+1, y]   + \
             -1.0 * a[x-1, y+1] + 1.0 * a[x+1, y+1]
        dy = -1.0 * a[x-1, y-1] - 2.0 * a[x, y-1] - 1.0 * a[x+1, y-1] + \
              1.0 * a[x-1, y+1] + 2.0 * a[x, y+1] + 1.0 * a[x+1, y+1]
        b[x, y] = min(int(math.sqrt(dx*dx + dy*dy) / 4.0), 255)
    return b

@wrap_numpy
def sobel_magnitude_numpy(a):
    dx = scipy.signal.convolve2d(a, numpy.array([[-1.0, 0.0, 1.0],
                                                 [-2.0, 0.0, 2.0],
                                                 [-1.0, 0.0, 1.0]]), 'same')
    dy = scipy.signal.convolve2d(a, numpy.array([[-1.0, -2.0, -1.0],
                                                 [ 0.0,  0.0,  0.0],
                                                 [ 1.0,  2.0,  1.0]]), 'same')
    return numpy.minimum(numpy.sqrt(dx*dx + dy*dy) / 4.0, 255).astype('B')
    
if __name__ == '__main__':
    from io import mplayer, view
    from time import time

    try:
        import pypyjit
        pypyjit.set_param(trace_limit=200000)
    except ImportError:
        pass

    start = start0 = time()
    for fcnt, img in enumerate(mplayer(Image, 'test.avi', '-benchmark')):
        #view(img)
        #view(sobel_magnitude(img))
        view(sobel_magnitude_numpy(img))
        print 1.0 / (time() - start), 'fps, ', (fcnt-2) / (time() - start0), 'average fps'
        start = time()
        if fcnt==2:
            start0 = time()
