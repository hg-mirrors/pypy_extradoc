
from itertools import imap, izip
import operator
import timeit

vector1 = [i for i in range(10000)]
vector2 = [i for i in range(10000)]

def one(vector1, vector2):
    return sum(imap(operator.add, vector1, vector2))

def two(vector1, vector2):
    return sum(x + y for x, y in izip(vector1, vector2))

def three(vector1, vector2):
    s = 0
    for i in range(len(vector1)):
        s += vector1[i] + vector2[i]
    return s

def four(vector1, vector2):
    return sum(vector1[i] + vector2[i] for i in range(len(vector1)))

def five(vector1, vector2):
    return sum([vector1[i] + vector2[i] for i in range(len(vector1))])

print "one", timeit.timeit(lambda : one(vector1, vector2), number=1000)
print "two", timeit.timeit(lambda : two(vector1, vector2), number=1000)
print "three", timeit.timeit(lambda : three(vector1, vector2), number=1000)
print "four", timeit.timeit(lambda : four(vector1, vector2), number=1000)
print "five", timeit.timeit(lambda : five(vector1, vector2), number=1000)

