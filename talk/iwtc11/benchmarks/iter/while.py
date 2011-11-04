from array import array

def _sum1d(a):
    sa = i = 0
    while i < len(a):
        sa += a[i]
        i += 1

def _xsum1d(a):
    sa = i = 0
    while i < len(a):
        sa += a[i] + i
        i += 1

def _wsum1d(a):
    sa = i = 0
    while i < len(a):
        sa += a[i] + len(a)
        i += 1
        
def _sum2d(a, w, h):
    sa = y = 0
    while y < h:
        x = 0
        while x < w:
            sa += a[y*w + x]
            x += 1
        y += 1

def _wsum2d(a, w, h):
    sa = y = 0
    while y < h:
        x = 0
        while x < w:
            sa += a[y*w + x] + w
            x += 1
        y += 1

def _xsum2d(a, w, h):
    sa = y = 0
    while y < h:
        x = 0
        while x < w:
            sa += a[y*w + x] + x
            x += 1
        y += 1
    sa = 0

def _whsum2d(a, w, h):
    sa = y = 0
    while y < h:
        x = 0
        while x < w:
            sa += a[y*w + x] + w + h
            x += 1
        y += 1
    sa = 0

def _xysum2d(a, w, h):
    sa = y = 0
    while y < h:
        x = 0
        while x < w:
            sa += a[y*w + x] + x + y
            x += 1
        y += 1

def _mean1d(a):
    sa = i = 0
    while i < len(a):    
        sa = (i*sa + a[i])/(i + 1.0);
        i += 1
        
def _median1d(a):
    sa = i = 0
    while i < len(a):
        if sa > a[i]:
            sa -= 1.0/(i + 1.0)
        elif sa < a[i]:
            sa += 1.0/(i + 1.0)
        i += 1

def _ripple1d(a):
    sa = i = 0
    while i < len(a):
        if sa > a[i]:
            sa -= 0.1
        elif sa < a[i]:
            sa += 0.1
        i += 1

def _ripple2d(a, w, h):
    sa = 0
    sa = y = 0
    while y < h:
        x = 0
        while x < w:
            if sa > a[y*w + x]:
                sa -= 0.1
            elif sa < a[y*w + x]:
                sa += 0.1
            x += 1
        y += 1

def sum1d(args):
    run1d(args, _sum1d)
    return "sum1d"

def xsum1d(args):
    run1d(args, _xsum1d)
    return "xsum1d"

def wsum1d(args):
    run1d(args, _wsum1d)
    return "wsum1d"

def sum2d(args):
    run2d(args, _sum2d)
    return "sum2d"

def wsum2d(args):
    run2d(args, _wsum2d)
    return "wsum2d"

def xsum2d(args):
    run2d(args, _xsum2d)
    return "xsum2d"

def whsum2d(args):
    run2d(args, _whsum2d)
    return "whsum2d"

def xysum2d(args):
    run2d(args, _xysum2d)
    return "xysum2d"

def mean1d(args):
    run1d(args, _mean1d, [1, -1])
    return "mean1d"

def median1d(args):
    run1d(args, _median1d, [1, -1])
    return "median1d"

def ripple1d(args):
    run1d(args, _ripple1d, [1, -1])
    return "ripple1d"

def ripple2d(args):
    run2d(args, _ripple2d, [1, -1])
    return "ripple2d"

def run1d(args, f, data=None):
    if data:
        a = array('d', data) * (100000000/len(data))
    else:
        a = array('d', [1]) * 100000000
    n = int(args[0])
    for i in xrange(n):
        f(a)
    return "sum1d"

def run2d(args, f, data=None):
    if data:
        a = array('d', data) * (100000000/len(data))
    else:
        a = array('d', [1]) * 100000000
    n = int(args[0])
    for i in xrange(n):
        f(a, 10000, 10000)
    return "sum1d"

if __name__ == '__main__':
    import sys
    eval(sys.argv[1])(sys.argv[2:])
    
