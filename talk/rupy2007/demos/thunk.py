from __pypy__ import thunk
def f():
    print 'computing...'
    return 6*7

x = thunk(f)
