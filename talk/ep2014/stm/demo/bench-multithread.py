from pyprimes import isprime
from Queue import Queue, Empty

subtotals = Queue()
queued = Queue()
nstarts = xrange(0, 5000000, 20000)
for nstart in nstarts:
    queued.put(nstart)

def f():
    while True:
        nstart = queued.get()
        subtotal = 0
        for n in xrange(nstart, nstart + 20000):
            if isprime(n):
                subtotal += 1
        subtotals.put(subtotal)

import thread
for j in range(2):
    thread.start_new_thread(f, ())

total = 0
for n in nstarts:
    total += subtotals.get()
print total
