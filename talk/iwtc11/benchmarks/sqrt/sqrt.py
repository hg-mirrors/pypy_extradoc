def sqrt(y, n=10000):
    x = y / 2
    while n > 0:
        #assert y > 0 and x > 0
        n -= 1
        x = (x + y/x) / 2
    return x

class Fix16(object):
    def __init__(self, val, scale=True):
        if isinstance(val, Fix16):
            self.val = val.val
        else:
            if scale:
                self.val = int(val * 2**16)
            else:
                self.val = val

    def __add__(self, other):
        return  Fix16(self.val + Fix16(other).val, False)

    def __sub__(self, other):
        return  Fix16(self.val - Fix16(other).val, False)

    def __mul__(self, other):
        return  Fix16((self.val >> 8) * (Fix16(other).val >> 8), False)

    def __div__(self, other):
        return  Fix16((self.val << 16) / Fix16(other).val, False)


    def __float__(self):
        return float(self.val) / float(2**16)

    def __int__(self):
        return self.val >> 16

    def __cmp__(self, other):
        return cmp(self.val, Fix16(other).val)

    def __str__(self):
        return str(float(self))

    __radd__ = __add__
    __rmul__ = __mul__
    def __rsub__(self, other):
        return  Fix16(Fix16(other).val - self.val, False)
    def __rdiv__(self, other):
        return  Fix16((Fix16(other).val << 16) / self.val, False)

def main(argv):
    sqrt(eval(argv[0])(123456), 100000000)
    return 'sqrt(%s)' % argv[0]
