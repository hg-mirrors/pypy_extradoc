from array import array

def binop(op):
    def f(a, b):
        if not isinstance(a, Image):
            a = ConstantImage(b.width, b.height, a)
        if not isinstance(b, Image):
            b = ConstantImage(a.width, a.height, b)

        out = a.new(typecode='d')
        for y in xrange(a.height):
            for x in xrange(a.width):
                out[x, y] = op(float(a[x, y]), float(b[x, y]))

        return out
    return f

class Image(object):
    def __init__(self, w, h, typecode='d', data=None):
        self.width = w
        self.height = h
        if data is None:
            self.data = array(typecode, [0]) * (w*h)
        else:
            self.data = data

    def new(self, w=None, h=None, typecode=None):
        if w is None:
            w = self.width
        if h is None:
            h = self.height
        if typecode is None:
            typecode = self.typecode
        return Image(w, h, typecode)

    def __getitem__(self, (x, y)):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y * self.width + x]
        return 0

    def __setitem__(self, (x, y), value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.data[y * self.width + x] = value

    __add__ = binop(float.__add__)
    __sub__ = binop(float.__sub__)
    __mul__ = binop(float.__mul__)
    __div__ = binop(float.__div__)
    __pow__ = binop(float.__pow__)

    __radd__ = binop(float.__radd__)
    __rsub__ = binop(float.__rsub__)
    __rmul__ = binop(float.__rmul__)
    __rdiv__ = binop(float.__rdiv__)
    __rpow__ = binop(float.__rpow__)

    __lt__ = binop(float.__lt__)
    __le__ = binop(float.__le__)
    __eq__ = binop(float.__eq__)
    __ne__ = binop(float.__ne__)
    __gt__ = binop(float.__gt__)
    __ge__ = binop(float.__ge__)

    def __nonzero__(self):
        return all(self.data)

class ConstantImage(Image):
    def __init__(self, w, h, value):
        self.width = w
        self.height = h
        self.value = value

    def __getitem__(self, (x, y)):
        return self.value

    def __setitem__(self, (x, y), value):
        raise TypeError('ConstantImage does not support item assignment')


def test_image():
    img = Image(10, 20)
    img[3, 4] = 7
    assert img[3, 4] == 7
    img[1, 2] = 42
    assert img[1, 2] == 42

    img2 = img + img
    assert img2[1, 2] == 84
    assert img2[3, 4] == 14

    img += 1
    assert img[2, 1] == 1
    assert img[3, 4] == 8
    assert img + img == 2 * img == img * 2
    assert not (2 * img == 3 * img)
    

