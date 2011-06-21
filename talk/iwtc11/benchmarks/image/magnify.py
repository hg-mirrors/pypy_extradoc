from plain import Image
from math import atan2, sqrt, sin, cos

def magnify(img):
    out = Image(img.width, img.height, typecode='B')
    out.data[:] = img.data
    maxr = img.height/3
    for y in xrange(img.height/2 - maxr, img.height/2 + maxr):
        for x in xrange(img.width/2 - maxr, img.width/2 + maxr):
            dx, dy = x - img.width/2, y - img.height/2
            a = atan2(dy, dx)
            r = sqrt(dx ** 2 + dy ** 2)
            if r < maxr:
                nr = r*r / maxr
                nx, ny = nr*cos(a), nr*sin(a)
                out[x,y] = img[int(nx) + img.width/2, int(ny) + img.height/2]
            else:
                out[x,y] = img[x,y]
    return out

if __name__ == '__main__':
    from io import mplayer, view
    import sys
    from time import time

    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = 'test.avi -vf scale=640:480 -benchmark'

    sys.setcheckinterval(2**30)
    try:
        import pypyjit
        pypyjit.set_param(trace_limit=200000)
    except ImportError:
        pass

    start = start0 = time()
    for fcnt, img in enumerate(mplayer(Image, fn)):
        view(magnify(img))
        print 1.0 / (time() - start), 'fps, ', (fcnt-2) / (time() - start0), 'average fps'
        start = time()
        if fcnt==2:
            start0 = time()
