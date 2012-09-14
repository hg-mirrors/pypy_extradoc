
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

class Labler(object):
    def __init__(self, seg):
        self.labels = seg.new()
        self.last_label = 0
        self.done = False

    def update(self, x, y, ll):
        neighbours = set(ll)
        neighbours.discard(0)
        if not neighbours:
            self.last_label += 1
            l = self.last_label
        else:
            l = min(neighbours)
        if self.labels[x, y] != l:
            self.done = False
        self.labels[x, y] = l

    def __getitem__(self, (x, y)):
        return self.labels[x, y]

    def renumber(self):
        ll = list(set(self.labels))
        ll.sort()
        if ll[0] != 0:
            ll.insert(0, 0)
        for x, y in self.labels.indexes():
            self.labels[x, y] = ll.index(self.labels[x, y])
        self.last_label = len(ll) - 1


def bwlabel(seg):
    labels = Labler(seg)
    while not labels.done:
        labels.done = True
        for x, y in seg.indexes():
            if seg[x, y]:
                ll = [labels[x, y], labels[x-1, y], labels[x-1, y-1],
                      labels[x, y-1], labels[x+1, y-1]]
                labels.update(x, y, ll)

        for x, y in reversed(seg.indexes()):
            if seg[x, y]:
                ll = [labels[x, y], labels[x+1, y], labels[x-1, y+1],
                      labels[x, y+1], labels[x+1, y+1]]
                labels.update(x, y, ll)

    labels.renumber()
    return labels.labels

@autoreload
def find_objects(fg):
    seg = erode(dilate(fg, 3), 4)
    labels = bwlabel(seg)
    viewsc(labels, 'segments')


