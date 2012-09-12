from subprocess import call, Popen
import os, time, re

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
    print
    print msg
    raw_input('Press ENTER')

def demo():
    with open('analytics.py', 'w') as fd:
        print >>fd, """
from reloader import ReloadHack
from io import view

class Tracker(ReloadHack):
    def update(self, frame):
        view(frame)
"""
    runner = Popen(['pypy', 'run.py', 'demo.avi'])
    vim = Vim('analytics.py')

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

    pause("That's all!")

    runner.kill()
if __name__ == '__main__':
    demo()
