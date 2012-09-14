from subprocess import call, Popen
import os, time, re, sys
import tempfile

class Vim(object):
    def __init__(self, *args):
        self.servername = 'DEMO_%d_%d' % (os.getpid(), id(self))
        self.tmp = tempfile.mktemp()
        with open(self.tmp, "w") as fd:
            print >>fd, """
syntax on
:set vb
set nocompatible

filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab
set softtabstop=4
autocmd FileType make set noexpandtab shiftwidth=8

:set backspace=indent,eol,start
"""
        call(['gvim', '--servername', self.servername, '-u', self.tmp] + list(args))

    def send(self, cmd):
        call(['gvim', '--servername', self.servername, '--remote-send', cmd])

    def type(self, cmd, delay=0.05):
        for c in re.findall('[^<>]|<.*?>', cmd):
            self.send(c)
            time.sleep(delay)

    def close(self):
        self.send('<ESC>:q!<CR>')
        os.unlink(self.tmp)

    def __del__(self):
        self.close()

def pause(msg=''):
    print "\n"
    print msg
    raw_input('Press ENTER\n')

def demo(skip1=False):
    if not skip1:
        with open('analytics.py', 'w') as fd:
            print >>fd, """
from reloader import ReloadHack
from io import view

class Tracker(ReloadHack):
    def update(self, frame):
        view(frame)
"""
    runner = Popen([sys.executable, 'run.py', 'demo.avi'])
    vim = Vim('analytics.py')

    if not skip1:
        part1(vim)
    part2(vim, skip1)

    runner.kill()
    vim.close()

def part1(vim):

    pause("We'r looking at the input and output of this Tracker object that\n" + 
          "currently simply returns it input. Let's modify it to make some\n" +
          "simple contrast adjustment.")
    vim.send('7gg$')
    vim.type('i * 2<ESC>:w<CR>', 0.2)

    pause("Now let's create a new class that estimates a background image\n" +
          "using a sliding mean.")
    with open('background.py', 'w') as fd:
        print >>fd, """
from reloader import ReloadHack

class Background(ReloadHack):
    def __init__(self):
        self.image = 0

    def update(self, frame):
        alfa = 0.9
        self.image = alfa * self.image + (1 - alfa) * frame
"""    
    vim.send(':e background.py<CR>')

    pause("Then, update Tracker to using the background estimater.")
    vim.send(':e analytics.py<CR>')
    vim.type('4ggifrom background import Background<CR><ESC>')
    vim.type('7ggOdef __init__(self):<CR>self.background = Background()<CR><ESC>')
    vim.type('11ggddOself.background.update(frame)<CR>view(self.background.image)<ESC>:w<CR>')

    pause("The moving objects are turned into ghosts. We need to increase the\n" +
          "window size to get a better estimate.")
    vim.send(':e background.py<CR>9gg')
    vim.type('A9<ESC>:w<CR>', 0.2)

    pause("We'r still getting ghost. Let's try to increase it even more.")
    vim.type('A9<ESC>:w<CR>', 0.2)

    pause("Now it's taking forever to converge. Let's make the window size\n" + 
          "depend on the number of frames observed.")
    vim.type('6ggOself.fcnt = 0<ESC>')
    vim.type('10ggOself.fcnt += 1<ESC>')
    vim.type('11ggA<BS><BS><BS><BS><BS>self.fcnt/(self.fcnt + 1.0)<ESC>:w<CR>')

    pause("That's better. Now, let's create a new function performing\n" + 
          "background subtraction,")
    with open('foreground.py', 'w') as fd:
        print >>fd, """
from reloader import autoreload

@autoreload
def foreground(img, bkg):
    return ((bkg - img) ** 2) > 40
"""
    vim.send(':e foreground.py<CR>')

    pause("and update Tracker to call it using the estimated background.")
    vim.send(':e analytics.py<CR>')
    vim.type('4ggofrom foreground import foreground<ESC>')
    vim.type('12ggofg = foreground(frame, self.background.image)<ESC>')
    vim.type('jI#<ESC>oview(255 * fg)<ESC>:w<CR>')

    pause("Wait a bit for the background to converge.")

    pause("That's a bit noisy. We'll have to increase the threashold a bit.")
    vim.send(':e foreground.py<CR>')
    vim.type('6ggA<BS><BS>100<ESC>:w<CR>', 0.2)

    pause("Still a bit noisy, let's increase it even more.")
    vim.type('6ggA<BS><BS><BS>200<ESC>:w<CR>', 0.2)

    pause("Now, let us start designing an object detector. First step would\n"+
          "be to implement dilation to get rid of small holes within\n"+
          "the objects,")

def part2(vim, skip1=False):
    with open('detect.py', 'w') as fd:
        print >>fd, """
from reloader import autoreload
from io import view, viewsc
from image import PixelIter

def dilate(fg, r=1):
    res = fg.new()
    for x, y in fg.indexes():
        res[x, y] = fg[x, y]
        for dx, dy in PixelIter(xrange(-r, r+1), xrange(-r, r+1)):
            res[x, y] = max(res[x, y], fg[x+dx, y+dy])
    return res

@autoreload
def find_objects(fg):
    seg = dilate(fg, 3)
    viewsc(seg, 'segments')

"""
    vim.send(':e detect.py<CR>')

    if not skip1:
        pause('and to call it from our tracker.')
        vim.send(':e analytics.py<CR>')
        vim.type('5ggofrom detect import find_objects<ESC>')
        vim.type('14ggofind_objects(fg)<ESC>:w<CR>')

    pause("That's a bit slow, but this operation is separable, let's see\n"+
          "if it is faster with two passes.")
    vim.send(':e detect.py<CR>')
    vim.type('7ggix<ESC>9ggix<ESC>jddOfor dx in xrange(-r, r+1):<ESC>')
    vim.type('11ggix<ESC>9wix<ESC>13wxxx', 0.2)
    vim.type('VkkkkyP5jx', 0.2)
    vim.type('14ggx7wcwxres<ESC>')
    vim.type('jbbbcwdy<ESC>jhx9wx6wcwxres<ESC>3wxxxllli+dy<ESC>:w<CR>', 0.2)

    pause("Now we need som erosion to thin out the objects again. Let's\n"+
          "generalize dilate make it implement both dilation and erotion")
    vim.type('6ggwcwmorph<ESC>$hi<BS><BS>, fn<ESC>')
    vim.type('11gg7wcwfn<ESC>', 0.2)
    vim.type('16gg7wcwfn<ESC>', 0.2)
    vim.type('19ggOdef dilate(fg, r=1):<CR>return morph(fg, r, max)<CR>')
    vim.type('<CR>def erode(fg, r=1):<CR>return morph(fg, r, min)<CR><ESC>')
    vim.type('G27ggwwierode(<ESC>A, 4)<ESC>:w<CR>')

    pause('Now, lets label each of the foreground pixels with one label\n' + 
          'per segment using a floodfill like algorithm')
    vim.type('25ggOdef bwlabel(seg):<CR>labels = seg.new()<CR>last_label = 0<CR>for x, y in seg.indexes():<CR>if seg[x, y]:<CR>ll = [labels[x, y], labels[x-1, y], labels[x-1, y-1],<CR>labels[x, y-1], labels[x+1, y-1]]<CR>neighbours = set(ll)<CR>neighbours.discard(0)<CR>if not neighbours:<CR>last_label += 1<CR>l = last_label<CR><BS>else:<CR>l = min(neighbours)<CR><BS>labels[x, y] = l<CR><BS><BS>return labels<CR><ESC>', 0.01)
    vim.type('G45ggOlabels = bwlabel(seg)<ESC>')
    vim.type('j4bcwlabels<ESC>:w<CR>', 0.2)

    pause("We'r getting several labels per object so lets try to repeat the\n" + 
          "floodfilling trversing the image in reversed order. But first, to\n" + 
          "prevent code duplication we're moving the common parts to a Labler class.")
    vim.type('25ggOclass Labler(object):<CR>def __init__(self, seg):<CR><CR><ESC>')
    vim.type('30ggVjxkkkPVj', 0.2)
    vim.send('>')
    vim.type('Iself.<ESC>jIself.<ESC>')
    vim.type('o<CR><BS>def update(self, x, y, ll):<ESC>')
    vim.type('38ggVjjjjjjjx', 0.2)
    vim.type('30ggpVjjjjjjj')
    vim.send('<')
    vim.type('34ggIself.<ESC>jiself.<ESC>')
    vim.type('38ggIself.<ESC>')
    vim.type('o<CR><BS>def __getitem__(self, (x, y)):<CR>return self.labels[x, y]<ESC>')
    vim.type('G45ggOlabels = Labler(seg)<ESC>')
    vim.type('49ggolabels.update(x, y, ll)<ESC>')
    vim.type('51ggA.labels<ESC>:w<CR>')

    pause("It still seems to work as before. Now lets add the second pass")
    vim.type('O<CR><BS><BS>for x, y in reversed(seg.indexes()):<CR>if seg[x, y]:<CR>ll = [labels[x, y], labels[x+1, y], labels[x-1, y+1],<CR>labels[x, y+1], labels[x+1, y+1]]<CR>labels.update(x, y, ll)<CR><ESC>:w<CR>', 0.01)

    pause("That's starting to look good, but in complicated cases we can still\n" + 
          "get multiple lables per segment, so we need to repeat until convergance")
    vim.type('56ggVkkkkkkkkkk', 0.2)
    vim.send('>')
    vim.type('Owhile not labels.done:<CR>labels.done = True<ESC>')
    vim.type('28ggoself.done = False<ESC>')
    vim.type('43gg39ggO<BS>if self.labels[x, y] != l:<CR>self.done = False<ESC>:w<CR>')

    pause("As a final touch, lets renumber the labels be consecutative\n" + 
          "integers.")
    vim.type('G63ggOlabels.renumber()<ESC>', 0.01)
    vim.type('44ggo<CR>def renumber(self):<CR>ll = list(set(self.labels))<CR>ll.sort()<CR>if ll[0] != 0:<CR>ll.insert(0, 0)<CR><BS>for x, y in self.labels.indexes():<CR>self.labels[x, y] = ll.index(self.labels[x, y])<CR><BS>self.last_label = len(ll) - 1<ESC>:w<CR>', 0.01)
       
    pause("Now, lets find a boudningbox for each segment,")
    vim.type("G75ggOclass BoundingBox(object):<CR>def __init__(self):<CR>self.maxx = self.maxy = float('-Inf')<CR>self.minx = self.miny = float('Inf')<CR><CR><BS>def add(self, x, y):<CR>self.maxx = max(self.maxx, x)<CR>self.maxy = max(self.maxy, y)<CR>self.minx = min(self.minx, x)<CR>self.miny = min(self.miny, y)<CR><BS><BS><CR>def extract_boxes(labels):<CR>boxes = [BoundingBox() for i in xrange(max(labels))]<CR>for x, y in labels.indexes():<CR>l = labels[x, y]<CR>if l:<CR>boxes[int(l-1)].add(x, y)<CR><BS><BS>return boxes<CR><ESC>", 0.01)
    vim.type("G98ggOboxes = extract_boxes(labels)<ESC>:w<CR>", 0.01)
    
    pause("and draw that boudning box.")
    vim.type("84ggo<BS><CR>def draw(self, img):<CR>for y in xrange(self.miny, self.maxy + 1):<CR>img[self.maxx, y] = 255<CR>img[self.minx, y] = 255<CR><BS>for x in xrange(self.minx, self.maxx + 1):<CR>img[x, self.miny] = 255<CR>img[x, self.maxy] = 255<CR><ESC>:w<CR>", 0.01)
    vim.type('108ggoreturn boxes<ESC>:w<CR>', 0.01)
    vim.type(':e analytics.py<CR>', 0.2)
    vim.type('15ggIfor box in <ESC>A:<CR>box.draw(frame)<CR><BS>view(frame)<ESC>')
    vim.type('19ggI#<ESC>:w<CR>')

    pause("The background model needs to converge again, but even after that\n"+
          "noise can sometimes create small detections. Lets discard them.")
    vim.send(':e detect.py<CR>')
    vim.type('75gg92ggo<BS><BS><CR>def area(self):<CR>return (self.maxx - self.minx + 1) * (self.maxy - self.miny + 1)<CR><ESC>', 0.01)
    vim.type('G108gg$hi, minarea=100<ESC>')
    vim.type('111ggoboxes = [b for b in boxes if b.area() ', 0.01)
    vim.send('>=')
    vim.type(' minarea]<ESC>:w<CR>', 0.01)

    pause("That's all! Feel free to make your own adjustments or (to quit),")


if __name__ == '__main__':
    demo(*map(eval, sys.argv[1:]))
