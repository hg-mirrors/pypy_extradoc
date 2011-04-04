from __future__ import generators
import pygame
from pygame.locals import *
import sys, os
from bubbob import pixmap
from bubbob.patmap import patmap
from bubbob import mnstrmap

SubtitlesLine = 0
#SubtitlesLine = 28

bwidth = 784
bheight = 592

pygame.init()
winstyle = HWSURFACE  # |FULLSCREEN
bestdepth = pygame.display.mode_ok((bwidth, bheight+SubtitlesLine), winstyle, 32)
screen = pygame.display.set_mode((bwidth, bheight+SubtitlesLine), winstyle,
                                 bestdepth)


class Ico:
    Cache = {}
    
    def __init__(self, filename, rect, filter=None, colorkey=0x010101):
        try:
            img = Ico.Cache[filename, filter]
        except KeyError:
            data = open(filename, 'rb').read()
            w, h, data = pixmap.decodepixmap(data)
            if filter:
                w, h, data = filter(w, h, data)
            img = pygame.image.fromstring(data, (w, h), "RGB")
            if colorkey is not None:
                img.set_colorkey(color(colorkey), RLEACCEL)
            Ico.Cache[filename, filter] = img
        if filter:
            rect = doublerect(rect)
        self.img = img.subsurface(rect)
        self.w, self.h = self.img.get_size()
    def draw(self, x, y):
        screen.blit(self.img, (x, y))

sprmap = {}

def doublesize(w, h, data):
    scanline = 3*w
    result = []
    for position in range(0, scanline*h, scanline):
        line = []
        for p in range(position, position+scanline, 3):
            line.append(2 * (data[p  ] + data[p+1] + data[p+2]))
        line = ''.join(line)
        result.append(line)
        result.append(line)
    return w*2, h*2, ''.join(result)

def doublerect((x, y, w, h)):
    return x*2, y*2, w*2, h*2

def sprget(n, filter=None, spriconcache={}):
    try:
        return spriconcache[n, filter]
    except KeyError:
        filename, rect = sprmap[n]
        ico = Ico(filename, rect, filter)
        spriconcache[n, filter] = ico
        return ico

def loadpattern(n):
    filename, rect = patmap[n]
    filename = os.path.join('pat', filename)
    bitmap = gamesrv.getbitmap(filename, keycol)
    return bitmap, rect

def patterns():
    for n in range(100):
        filename, rect = patmap[n, 0, 0]
        filename = os.path.join('bubbob', 'pat', filename)
        ico1 = Ico(filename, rect)
        x, y, w, h = rect
        ico2 = Ico(filename, (x, y, 16, 16), pixmap.makebkgnd, colorkey=None)
        yield ico1, ico2

try:
    import psyco
except ImportError:
    pass
else:
    psyco.bind(doublesize)
    psyco.bind(pixmap.makebkgnd)

class GoToFrame:
    pass

class Board:
    TargetFrame = 1
    subtitle = ''
    
    def __init__(self, last=None):
        self.wallico, self.bkgndico = Patterns.next()
        if last is None:
            sprites = []
        else:
            sprites = b.sprites[:b.sprites.index(last)+1]
        self.sprites = sprites

    def insertbefore(self, s1, s2):
        self.sprites.remove(s1)
        i = self.sprites.index(s2)
        self.sprites.insert(i, s1)

    def draw(self):
        for x in range(24, bwidth-16, 32):
            for y in range(24, bheight-16, 32):
                self.bkgndico.draw(x,y)
        for x in range(0, bwidth, 16):
            self.wallico.draw(x, 0)
        for y in range(16, bheight-16, 16):
            self.wallico.draw(0, y)
            self.wallico.draw(bwidth-16, y)
        screen.fill((0, 0, 0), (0, bheight, 16, 16))
        for x in range(0, bwidth, 16):
            self.wallico.draw(x, bheight-16)

        for s in self.sprites:
            s.draw()
        if SubtitlesLine > 0:
            draw_subtitle(self.subtitle)
        pygame.display.flip()

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                Board.TargetFrame = int(Board.CurFrame-0.5)
                if Board.TargetFrame < 0:
                    Board.TargetFrame = 0
                return 1
            if event.key == K_RIGHT:
                Board.TargetFrame = int(Board.CurFrame+1)
                return 1
            if event.key == K_SPACE:
                return 1
        if event.type == QUIT:
            raise SystemExit
        return 0

    def animate(self, msg, pausing=1):
        while 1:
            if msg.startswith('+'):
                msg = msg[1:]
                self.subtitle = msg.strip()
            else:
                self.subtitle = ''
            stop = None
            clock = pygame.time.Clock()
            progress = 1
            Board.CurFrame += 0.5
            while not stop and progress:
                if Board.TargetFrame is None:
                    self.draw()
                    clock.tick(9)
                    e = pygame.event.poll()
                    if e:
                        self.handle(e)
                progress = 0
                for s in self.sprites[:]:
                    for g in s.gen[:]:
                        try:
                            stop = g.next() or stop
                        except StopIteration:
                            s.gen.remove(g)
                        else:
                            progress = 1
            self.pause(msg, pausing)
            if not (isinstance(stop, str) and stop.startswith("pause")):
                break
            msg = stop[5:]
            pausing = 1

    def pause(self, msg, pausing=1):
        self.subtitle = msg.strip()
        Board.CurFrame = int(Board.CurFrame+1)
        while 1:
            if Board.TargetFrame is None:
                self.draw()
                if pausing:
                    e = pygame.event.wait()
                    while not self.handle(e):
                        e = pygame.event.wait()
                if Board.TargetFrame is None:
                    break
            pausing = 1
            if Board.TargetFrame == Board.CurFrame:
                Board.TargetFrame = None
                continue
            if Board.TargetFrame < Board.CurFrame:
                raise GoToFrame()
            break

# ____________________________________________________________

class Sprite:
    imgsetter = None
    run = None
    
    def __init__(self, x, y, ico=None):
        self.x = x
        self.y = y
        self.ico = ico
        self.gen = []
        if self.run is not None:
            self.gen.append(self.run())
        b.sprites.append(self)

    def setimages(self, gen):
        if self.imgsetter is not None:
            self.gen.remove(self.imgsetter)
        self.imgsetter = gen
        if gen is not None:
            self.gen.append(gen)

    def draw(self):
        if self.ico:
            self.ico.draw(self.x, self.y)

    def move(self, x, y, ico=None):
        self.x = x
        self.y = y
        if ico:
            self.ico = ico

    def step(self, dx, dy):
        self.x += dx
        self.y += dy

    def seticon(self, ico):
        self.ico = ico

    def kill(self):
        b.sprites.remove(self)

    def revive(self, dx=0, dy=0):
        del self.gen[:]
        b.sprites.append(self)
        if dx or dy:
            self.gen.append(self.straightline(self.x+dx, self.y+dy))

    def cyclic(self, nimages, speed=5, filter=None):
        images = [sprget(n, filter) for n in nimages]
        speed = range(speed)
        while 1:
            for img in images:
                self.seticon(img)
                for i in speed:
                    yield None

    def straightline(self, x, y, steps=5):
        for i in range(steps):
            f = 1.5 / (steps-i)
            self.move(int(f*x + (1-f)*self.x),
                      int(f*y + (1-f)*self.y))
            yield None

    def walkabit(self, n, dx, dy):
        for i in range(n):
            self.step(dx, dy)
            yield None
        yield "stop"

    def stopafter(self, delay):
        for i in range(delay):
            yield None
        yield "stop"

    def die(self, delay):
        for i in range(delay):
            yield None
        self.kill()

    def ontop(self):
        b.sprites.remove(self)
        b.sprites.append(self)

# ____________________________________________________________

FONT = 'cyrvetic.ttf'
FONT2 = 'VeraMoBd.ttf'

def getfont(size, bold, font):
    font = pygame.font.Font(font, size)
    font.set_bold(bold)
    return font

def color(c):
    return c >> 16, (c >> 8) & 0xFF, c & 0xFF

def colorstep(current, target, f):
    r1, g1, b1 = color(current)
    r2, g2, b2 = color(target)
    r = f*r2 + (1-f)*r1
    g = f*g2 + (1-f)*g1
    b = f*b2 + (1-f)*b1
    return (int(r) << 16) | (int(g) << 8) | int(b)

def draw_subtitle(s):
    screen.fill((0, 0, 0), (0, bheight+5, bwidth, SubtitlesLine-5))
    if s:
        font = getfont(16, 0, FONT2)
        imgs = [font.render(line, 0, (255, 255, 255), (0, 0, 60))
                for line in s.split('\n')]
        imgs.reverse()
        y = bheight+SubtitlesLine
        for img in imgs:
            w, h = img.get_size()
            y -= h
            screen.blit(img, ((bwidth-w)//2, y))

class Line(Sprite):
    TextCache = {}
    
    def __init__(self, x, y, text, size, bold=1, font=FONT, color=0xFFFFFF):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.bold = bold
        self.font = font
        self.color = color
        self.gen = []
        self.setup()
        b.sprites.append(self)

    def setup(self):
        pass

    def render(self):
        text = self.text
        if '\x00' in text:
            i = text.index('\x00')
            ico = eval(text[i+1:])
            text = text[:i]
        else:
            ico = None
        key = (text, self.size, self.bold, self.font, self.color, ico)
        try:
            return Line.TextCache[key]
        except KeyError:
            font = getfont(self.size, self.bold, self.font)
            img = font.render(text or ' ', 1, color(self.color))
            if ico is not None:
                ico = sprget(ico)
                w, h = img.get_size()
                s = pygame.Surface((w+ico.w, max(h,ico.h)))
                s.fill((1,1,1))
                s.blit(img, (0,0))
                s.blit(ico.img, (w,0))
                s.set_colorkey((1,1,1))
                img = s
            Line.TextCache[key] = img
            return img

    def draw(self):
        img = self.render()
        screen.blit(img, (self.x, self.y))

    def shiftcolor(self, target, steps, delay=0):
        for i in range(delay):
            yield None
        for i in range(steps):
            f = float(i+1) / steps
            self.color = colorstep(self.color, target, f)
            yield None


class CenterLine(Line):
    def setup(self):
        w, h = self.render().get_size()
        self.x -= w//2

class HeadLine(CenterLine):
    def setup(self):
        CenterLine.setup(self)
        Line(self.x+4, self.y+4, self.text, self.size,
             self.bold, self.font, color = 0x000000)

class Frame(Sprite):
    shadow = 6
    
    def __init__(self, x, y, w, h, bgcolor=0xFFFFFF):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bgcolor = bgcolor
        self.gen = []
        self.setup()
        b.sprites.append(self)
        
    def setup(self):
        pass
    
    def draw(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        screen.fill(color(self.bgcolor), (x, y, w, h))
        shadow = color(0x000000)
        s = self.shadow
        screen.fill(shadow, (x+s, y+h, w, s))
        screen.fill(shadow, (x+w, y+s, s, h-s))

class Program:
    
    def __init__(self, x, y, text, bgcolor=0xFFFFFF):
        self.x = x
        self.y = y
        lines = text.split('\n')
        if not lines[0]: del lines[0]
        allspr = []
        y0 = y
        for line in lines:
            if line:
                allspr.append(Line(x, y, line, 20, 0,
                                   font=FONT2, color=0x000000))
            y += 48
        maxw = max([s.render().get_size()[0] for s in allspr])
        self.s = Frame(x-20, y0-20, maxw+40, y-y0-40, bgcolor=bgcolor)
        b.insertbefore(self.s, allspr[0])
        self.allspr = allspr + [self.s]

    def getcoord(self, linenum):
        return (self.x - 12, self.y + 48*linenum - 29)

class ProgramRunner(Sprite):
    
    def __init__(self, program, state, images, steps):
        x, y = program.getcoord(0)
        Sprite.__init__(self, x, y, sprget(images[0]))
        self.setimages(self.cyclic(images, 1))
        self.program = program
        self.state = state
        self.steps = steps
        
    def go(self, linenum):
        x, y = self.program.getcoord(linenum)
        for t in self.straightline(x, y):
            yield t

    def run(self):
        for state in self.steps:
            if isinstance(state, str) and state.startswith("pause"):
                yield state
            else:
                linenum, statechanges = state
                self.state.change(statechanges)
                for t in self.go(linenum):
                    yield t
                yield None
        yield "stop"

class StateFrame(Frame):
    font = FONT2
    size = 20
    liney0 = 35

    def __init__(self, x, y, example, nblines, bgcolor, format = '%s = %s'):
        self.format = format
        wmax = 0
        for keyvalue in example.items():
            s = Line(0, 0, self.format % keyvalue, self.size, 0, self.font)
            w, h = s.render().get_size()
            if w > wmax: wmax = w
        self.hstep = h+12
        s.kill()
        Frame.__init__(self, x, y, wmax+30, nblines*self.hstep+50, bgcolor)
        self.state = {}

    def change(self, nstate):
        for key, value in nstate.items():
            if isinstance(key, LogFrame):
                key.log(value)
                continue
            try:
                line = self.state[key]
            except KeyError:
                line = Line(self.x + 15,
                            self.y + len(self.state)*self.hstep + self.liney0,
                            '', self.size, 0, self.font, self.bgcolor)
                self.state[key] = line
            self.gen.append(self.blink(line, key, value))

    def blink(self, line, key, value):
        if callable(value):
            for t in value(line, key):
                yield t
            return
            
        for t in line.shiftcolor(self.bgcolor, 3):
            yield t
        if value is None:
            return
        fgcolor = 0x000000
        if (isinstance(value, tuple) and len(value) == 2
            and isinstance(value[0], int)):
            fgcolor, value = value
        line.text = self.format % (key, value)
        for t in line.shiftcolor(fgcolor, 3):
            yield t

    def kill(self):
        for key, line in self.state.items():
            line.kill()
        Frame.kill(self)

class LogFrame(Frame):
    font = FONT2
    size = 20

    def __init__(self, x, y, example, nblines, bgcolor=0xFFFF80, interline=12):
        s = Line(0, 0, example, self.size, 0, self.font)
        w, h = s.render().get_size()
        self.hstep = h+interline
        s.kill()
        Frame.__init__(self, x, y, w+60, nblines*self.hstep+10, bgcolor)
        self.lines = []
        self.nblines = nblines

    def append(self, text, immed=1):
        fgcolor = 0x000000
        if (isinstance(text, tuple) and len(text) == 2
            and isinstance(text[0], int)):
            fgcolor, text = text
        self.lines.append(Line(self.x+44, self.y, text, self.size, 0, self.font,
                               self.bgcolor))
        if len(self.lines) > self.nblines:
            self.lines.pop(0).kill()
        if immed:
            self.lines[-1].color = fgcolor
            lines = list(self.lines)
            lines.reverse()
            y = self.y + self.h
            for line in lines:
                y -= self.hstep
                line.move(line.x, y)
        return fgcolor

    def log(self, text):
        self.gen.append(self.insertline(text))

    def insertline(self, text):
        fgcolor = self.append(text, 0)
        lines = [(line, line.color) for line in self.lines]
        lines[-1] = (self.lines[-1], fgcolor)
        rng = range(0, self.hstep, 10)
        rng.reverse()
        lines.reverse()
        for dy in rng:
            f = 1.0 - float(dy)/self.hstep
            y = self.y + self.h + dy
            for line, targetcolor in lines:
                y -= self.hstep
                line.move(line.x, y)
                line.color = colorstep(line.color, targetcolor, f)
            yield None

    def kill(self):
        for line in self.lines:
            line.kill()
        Frame.kill(self)

    def revive(self, dx=0, dy=0):
        Frame.revive(self, dx, dy)
        for line in self.lines:
            line.revive(dx, dy)

    def ontop(self):
        Frame.ontop(self)
        for line in self.lines:
            line.ontop()

# ____________________________________________________________

MAX = 10

from bubbob.sprmap import sprmap as localmap

for key, (filename, rect) in localmap.items():
    filename = os.path.join('bubbob', 'images', filename)
    if filename.find('%d') >= 0:
        for i in range(MAX):
            sprmap[key+1000*i] = (filename % i, rect)
    else:
        sprmap[key] = (filename, rect)

localmap = {
    ('lem-walk', 1,0) :  ('image1.ppm', (  0,  0, 32, 32)),
    ('lem-walk', 1,1) :  ('image1.ppm', ( 32,  0, 32, 32)),
    ('lem-walk', 1,2) :  ('image1.ppm', ( 64,  0, 32, 32)),
    ('lem-walk', 1,3) :  ('image1.ppm', ( 96,  0, 32, 32)),
    ('lem-walk', 1,4) :  ('image1.ppm', (128,  0, 32, 32)),
    ('lem-walk', 1,5) :  ('image1.ppm', (160,  0, 32, 32)),
    ('lem-walk', 1,6) :  ('image1.ppm', (192,  0, 32, 32)),
    ('lem-walk', 1,7) :  ('image1.ppm', (224,  0, 32, 32)),
    ('lem-fall', 1,0) :  ('image1.ppm', (256,  0, 32, 32)),
    ('lem-fall', 1,1) :  ('image1.ppm', (288,  0, 32, 32)),
    ('lem-fall', 1,2) :  ('image1.ppm', (320,  0, 32, 32)),
    ('lem-fall', 1,3) :  ('image1.ppm', (352,  0, 32, 32)),

    ('lem-fall',-1,3) :  ('image2.ppm', (  0,  0, 32, 32)),
    ('lem-fall',-1,2) :  ('image2.ppm', ( 32,  0, 32, 32)),
    ('lem-fall',-1,1) :  ('image2.ppm', ( 64,  0, 32, 32)),
    ('lem-fall',-1,0) :  ('image2.ppm', ( 96,  0, 32, 32)),
    ('lem-walk',-1,7) :  ('image2.ppm', (128,  0, 32, 32)),
    ('lem-walk',-1,6) :  ('image2.ppm', (160,  0, 32, 32)),
    ('lem-walk',-1,5) :  ('image2.ppm', (192,  0, 32, 32)),
    ('lem-walk',-1,4) :  ('image2.ppm', (224,  0, 32, 32)),
    ('lem-walk',-1,3) :  ('image2.ppm', (256,  0, 32, 32)),
    ('lem-walk',-1,2) :  ('image2.ppm', (288,  0, 32, 32)),
    ('lem-walk',-1,1) :  ('image2.ppm', (320,  0, 32, 32)),
    ('lem-walk',-1,0) :  ('image2.ppm', (352,  0, 32, 32)),

    ('lem-jail',   0) :  ('image4.ppm', (  0,  0, 32, 32)),
    ('lem-jail',   1) :  ('image4.ppm', (  0, 32, 32, 32)),
    ('lem-jail',   2) :  ('image4.ppm', (  0, 64, 32, 32)),
    }
for n in range(16):
    localmap[('lem-crash', n)] = ('image3.ppm', (32*n, 0, 32, 32))

for key, (filename, rect) in localmap.items():
    filename = os.path.join('bubbob', 'ext5', filename)
    sprmap[key] = (filename, rect)

# ____________________________________________________________

def run():
    global Patterns
    while 1:
        Patterns = patterns()
        Board.CurFrame = 0
        try:
            execfile('def.py', globals(), globals())
        except GoToFrame:
            continue
        else:
            break

if len(sys.argv) > 1:
    Board.TargetFrame = int(sys.argv[1])
try:
    run()
finally:
    print Board.CurFrame
