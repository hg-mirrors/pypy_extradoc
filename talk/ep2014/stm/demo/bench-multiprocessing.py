from pyprimes import isprime
from multiprocessing import Pool

def process(nstart):
    subtotal = 0
    for n in xrange(nstart, nstart + 20000):
        if isprime(n):
            subtotal += 1
    return subtotal

pool = Pool(4)
results = pool.map(process, xrange(0, 5000000, 20000))
total = sum(results)

print total
