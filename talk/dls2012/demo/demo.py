from subprocess import call, Popen
import os, time, re, sys

class Vim(object):
    def __init__(self, *args):
        self.servername = 'DEMO_%d_%d' % (os.getpid(), id(self))
        call(['gvim', '--servername', self.servername] + list(args))

    def send(self, cmd):
        call(['gvim', '--servername', self.servername, '--remote-send', cmd])

    def type(self, cmd, delay=0.05):
        for c in re.findall('[^<>]|<.*?>', cmd):
            self.send(c)
            time.sleep(delay)

    def __del__(self):
        self.send('<ESC>:q!<CR>')

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

def dilate(fg, r=1):
    res = fg.new()
    for x, y in fg.indexes():
        res[x, y] = fg[x, y]

        for dx in xrange(-r, r+1):
            for dy in xrange(-r, r+1):
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
    vim.type('6ggix<ESC>9ggix<ESC>jjdd')
    vim.send('<<')
    vim.type('ix<ESC>9wix<ESC>13wxxx', 0.2)
    vim.type('VkkkkkyP6jx')
    vim.type('15ggx7wcwxres<ESC>')
    vim.type('jbbbcwdy<ESC>jhx9wx6wcwxres<ESC>3wxxxllli+dy<ESC>:w<CR>', 0.2)

    pause("Now we need som erosion to thin out the objects again. Let's\n"+
          "generalize dilate make it implement both dilation and erotion")
    vim.type('5ggwcwmorph<ESC>$hi<BS><BS>, fn<ESC>')
    vim.type('11gg7wcwfn<ESC>', 0.2)
    vim.type('17gg7wcwfn<ESC>', 0.2)
    vim.type('20ggOdef dilate(fg, r=1):<CR>return morph(fg, r, max)<CR>')
    vim.type('<CR>def erode(fg, r=1):<CR>return morph(fg, r, min)<CR><ESC>')
    vim.type('28ggwwierode(<ESC>A, 4)<ESC>:w<CR>')

    pause("That's all! Feel free to make your own adjustments or (to quit),")


    runner.kill()
if __name__ == '__main__':
    demo(*map(eval, sys.argv[1:]))
