
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

class BoundingBox(object):
    def __init__(self):
        self.maxx = self.maxy = float('-Inf')
        self.minx = self.miny = float('Inf')

    def add(self, x, y):
        self.maxx = max(self.maxx, x)
        self.maxy = max(self.maxy, y)
        self.minx = min(self.minx, x)
        self.miny = min(self.miny, y)

    def draw(self, img):
        for y in xrange(self.miny, self.maxy + 1):
            img[self.maxx, y] = 255
            img[self.minx, y] = 255
        for x in xrange(self.minx, self.maxx + 1):
            img[x, self.miny] = 255
            img[x, self.maxy] = 255

    def area(self):
        return (self.maxx - self.minx + 1) * (self.maxy - self.miny + 1)



def extract_boxes(labels):
    boxes = [BoundingBox() for i in xrange(int(max(labels)))]
    for x, y in labels.indexes():
        l = labels[x, y]
        if l:
            boxes[int(l-1)].add(x, y)
    return boxes

@autoreload
def find_objects(fg, minarea=100):
    seg = erode(dilate(fg, 3), 4)
    labels = bwlabel(seg)
    boxes = extract_boxes(labels)
    boxes = [b for b in boxes if b.area() >= minarea]
    viewsc(labels, 'segments')
    return boxes


