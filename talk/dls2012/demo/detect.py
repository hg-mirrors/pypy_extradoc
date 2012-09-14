
from reloader import autoreload
from io import view, viewsc
from image import PixelIter

def morph(fg, r, fn):
    xres = fg.new()
    for x, y in fg.indexes():
        xres[x, y] = fg[x, y]
        for dx in xrange(-r, r+1):
            xres[x, y] = fn(xres[x, y], fg[x+dx, y])
    res = fg.new()
    for x, y in fg.indexes():
        res[x, y] = xres[x, y]
        for dy in xrange(-r, r+1):
            res[x, y] = fn(res[x, y], xres[x, y+dy])
    return res

def dilate(fg, r=1):
    return morph(fg, r, max)

def erode(fg, r=1):
    return morph(fg, r, min)

@autoreload
def find_objects(fg):
    seg = erode(dilate(fg, 3), 4)
    viewsc(seg, 'segments')


