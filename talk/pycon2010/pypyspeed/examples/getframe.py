
import sys

GLOBAL = 10000000

def f():
    k = 0
    i = 0
    while i < GLOBAL:
        if k:
            i += 2
        sys._getframe()
        i += 1

f()
