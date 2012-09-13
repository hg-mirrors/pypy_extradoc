from reloader import autoreload
from io import view

def morph(fg, r, fn):
    res = fg.new()
    for y in xrange(fg.height):
        for x in xrange(fg.width):
            #res[x, y] = max(fg[x+dx, y+dy] 
            #                for dx in xrange(-r, r+1) 
            #                for dy in xrange(-r, r+1))
            res[x, y] = fg[x, y]
            for dx in xrange(-r, r+1):
                for dy in xrange(-r, r+1):
                    res[x, y] = fn(res[x, y], fg[x+dx, y+dy])
    return res

def morph(fg, r, fn):
    xres = fg.new()
    for y in xrange(fg.height):
        for x in xrange(fg.width):
            xres[x, y] = fg[x, y]
            for dx in xrange(-r, r+1):
                xres[x, y] = fn(xres[x, y], fg[x+dx, y])
    res = fg.new()
    for y in xrange(fg.height):
        for x in xrange(fg.width):
            res[x, y] = xres[x, y]
            for dy in xrange(-r, r+1):
                res[x, y] = fn(res[x, y], xres[x, y+dy])
    return res

def erode(fg, r=1):
    return morph(fg, r, min)

def dilate(fg, r=1):
    return morph(fg, r, max)

@autoreload
def find_objects(fg):
    seg = erode(dilate(fg, 3), 4)
    view(255*seg, 'd')
