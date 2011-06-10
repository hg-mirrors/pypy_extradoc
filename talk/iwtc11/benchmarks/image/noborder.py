from array import array

class NoBorderImage(object):
    "An image class for people who dont care about border effects"
    
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.data = array('d', [0]) * (w*h)

    def _idx(self, p):
        if isinstance(p, Pixel):
            idx = p.idx
        else:
            idx = p[1] * self.width + p[0]
        return min(max(idx, 0), len(self.data)-1)

    def __getitem__(self, p):
        return self.data[self._idx(p)]

    def __setitem__(self, p, val):
        self.data[self._idx(p)] = val

    def pixels(self):
        for i in xrange(self.width * self.height):
            yield Pixel(i, self.width)

    def pixeliter(self):
        return PixelIter(self.width, self.height)

class Pixel(object):
    def __init__(self, idx, w):
        self.idx = idx
        self.width = w

    def __add__(self, other):
        return Pixel(self.idx + other[1]*self.width + other[0], self.width)

class PixelIter(object):
    def __init__(self, w, h):
        self.width = w
        self.n = w*h
        self.idx = 0
        
    def __iter__(self):
        return self

    def next(self):
        idx = self.idx
        self.idx += 1
        if idx >=self.n:
            raise StopIteration
        return Pixel(idx, self.width)

def conv3x3(img, k):
    assert k.width == k.height == 3
    res = NoBorderImage(img.width, img.height)
    for p in img.pixels():
        res[p] = k[2,2]*img[p + (-1, -1)] + k[1,2]*img[p + (0, -1)] + k[0,2]*img[p + (1, -1)] + \
                 k[2,1]*img[p + (-1,  0)] + k[1,1]*img[p + (0,  0)] + k[0,1]*img[p + (1,  0)] + \
                 k[2,0]*img[p + (-1,  1)] + k[1,0]*img[p + (0,  1)] + k[0,0]*img[p + (1,  1)]
    return res

def conv3x3iter(img, k):
    assert k.width == k.height == 3
    res = NoBorderImage(img.width, img.height)
    for p in img.pixeliter():
        res[p] = k[2,2]*img[p + (-1, -1)] + k[1,2]*img[p + (0, -1)] + k[0,2]*img[p + (1, -1)] + \
                 k[2,1]*img[p + (-1,  0)] + k[1,1]*img[p + (0,  0)] + k[0,1]*img[p + (1,  0)] + \
                 k[2,0]*img[p + (-1,  1)] + k[1,0]*img[p + (0,  1)] + k[0,0]*img[p + (1,  1)]
    return res

if __name__ == '__main__':
    try:
        import pypyjit
        pypyjit.set_param(trace_limit=200000)
    except ImportError:
        pass

    import time
    a = time.time()
    for i in range(10):
        conv3x3iter(NoBorderImage(100, 100), NoBorderImage(3,3))
    b = time.time()
    print 'NoBorderImage:', b - a

