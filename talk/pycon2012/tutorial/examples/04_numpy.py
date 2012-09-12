try:
    import numpypy
except ImportError:
    pass
import numpy

def f():
    a = numpy.zeros(10000, dtype=float)
    b = numpy.zeros(10000, dtype=float)
    c = numpy.zeros(10000, dtype=float)
    (a + b)[0] = 3
    (a + b * c)[0] = 3
    (a + b * c).sum()

f()
