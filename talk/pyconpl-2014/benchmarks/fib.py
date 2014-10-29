
import time
import numpy
try:
    from matplotlib import pylab
except:
    from embed.emb import import_mod
    pylab = import_mod('matplotlib.pylab')

def fib(n):
    if n == 0 or n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)

def f():
    for i in range(10000):
        "".join(list(str(i)))

times = []
for i in xrange(1000):
    t0 = time.time()
    #f()
    fib(17)
    times.append(time.time() - t0)

hist, bins = numpy.histogram(times, 20)
#pylab.plot(bins[:-1], hist)
pylab.ylim(0, max(times) * 1.2)
pylab.plot(numpy.array(times))
#pylab.hist(hist, bins, histtype='bar')
pylab.show()
