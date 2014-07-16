from pyprimes import isprime

total = 0
for n in xrange(5000000):
    if isprime(n):
        total += 1

print total
