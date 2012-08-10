
def hwall(x, y, cnt):
    for i in range(cnt):
        b.sprites.append(Sprite(x, y, b.wallico))
        x += 16

def vwall(x, y, cnt):
    for i in range(cnt):
        b.sprites.append(Sprite(x, y, b.wallico))
        y += 16

Player = mnstrmap.GreenAndBlue.players[5]
Player = Player[3:6]
sprmap['py'] = ('pycon.ppm', (0, 0, 32, 32))

class MyRunner(ProgramRunner):
    
    def __init__(self, x, y, stateexample, statelines, program, states):
        self.st = StateFrame(x, y+64, stateexample, statelines,
                             self.statebgcolor, self.stateformat)
        self.mascotte = Sprite(x, y, sprget(self.images[-1], doublesize))
        ProgramRunner.__init__(self, program, self.st, self.images, states)

    def kill(self):
        self.st.kill()
        self.mascotte.kill()
        ProgramRunner.kill(self)

class RunCPython(MyRunner):
    statebgcolor = 0xC0C0C0
    images = mnstrmap.Nasty.right
    stateformat = '%s = %s'

#class RunSpace(MyRunner):
#    statebgcolor = 0xFF8080
#    images = Player
#    stateformat = '%s <- %s'

COMPRESSED = 0

class Bookkeeper(LogFrame):
    image = mnstrmap.Monky.right[0], None
    sdx = +6
    sdy = -40
    bgcolor = 0xFFFF80
    from_right = 0
    def __init__(self, x, y, example, nblines=None):
        if COMPRESSED:
            nblines = nblines or 9
            interline = 5
        else:
            nblines = nblines or 7
            interline = 12
        LogFrame.__init__(self, x, y, example, nblines=nblines,
                          bgcolor=self.bgcolor, interline=interline)
        self.s = Sprite(x + self.w*self.from_right + self.sdx,
                        y + self.h + self.sdy,
                        sprget(*self.image))
    def kill(self):
        self.s.kill()
        LogFrame.kill(self)
    def revive(self, dx=0, dy=0):
        LogFrame.revive(self, dx, dy)
        self.s.revive(dx, dy)

class Codemaker(Bookkeeper):
    image = mnstrmap.Springy.right[0], None

class DarkerCodemaker(Codemaker):
    bgcolor = 0xD0D060

class CPU(Bookkeeper):
    bgcolor = 0xC080FF
    image = ('lem-walk', 1, 0), doublesize
    sdx = -6
    sdy = -72

class CPU_Right(CPU):
    bgcolor = 0xC080FF
    image = ('lem-walk', -1, 0), doublesize
    sdx = -56
    sdy = -72
    from_right = 1

class CPU_Nowhere(CPU_Right):
    sdy = -9999


class TextFrame(LogFrame):
    shadow = 3

    def __init__(self, x, y, text, bgcolor):
        text += '  '
        LogFrame.__init__(self, x, y, text, 1, bgcolor)
        self.append(text)


class Space(Frame):
    hack = 169

    def __init__(self, x=200, y=370):
        Frame.__init__(self, x, y, 520, 210, self.bgcolor)
        self.mascotte = Sprite(x+420, y-64, sprget(self.images[-1], doublesize))
        self.operations = [
            TextFrame(x+220, y+25, '__add__', self.opcolor),
            TextFrame(x+220, y+85, '__getitem__', self.opcolor),
            TextFrame(x+220, y+145, '__getattribute__', self.opcolor),
            #TextFrame(x+220, y+205, '__hash__', self.opcolor),
            ]
        #for i in range(10,-1,-5):
        #    t = TextFrame(x+20+i, y+145+i*2, '__getattribute__', self.opcolor)
        self.linepos = {}

    def goto(self, yline, steps=15):
        def anim(line, key):
            newline = Line(line.x+77, line.y, line.text[len(key)+3:], line.size,
                           line.bold, line.font, 0xFF0000)
            op = self.operations[int(yline+0.5)]
            op.ontop()
            self.linepos[yline] = line.x, line.y
            x2 = self.x+240
            y2 = self.y+30+int(yline*60)
            for t in newline.straightline(x2, y2, steps):
                yield t
            newline.kill()
        return anim

    def comefrom(self, yline, value, steps=12):
        def anim(line, key):
            line.text = line.text[:len(key)+3]
            newline = Line(self.x+240, self.y+30+yline*60, str(value), line.size,
                           line.bold, line.font, 0xFF0000)
            op = self.operations[int(yline+0.5)]
            op.ontop()
            for t in newline.straightline(newline.x, newline.y+60):
                yield t
            for t in newline.straightline(line.x+self.hack, line.y, steps):
                yield t
            line.text += '      ' + str(value)
            newline.kill()
        return anim

    def compute(self, yline):
        def anim(line, key):
            op = self.operations[int(yline+0.5)]
            opbg = op.bgcolor
            for t in range(4):
                op.bgcolor = 0xFF8080
                for i in range(2): yield None
                op.bgcolor = opbg
                for i in range(2): yield None
        return anim


class StdObjSpace(Space):
    bgcolor = 0x8080FF
    opcolor = 0xD0D0FF
    images  = mnstrmap.Orcy.left

class FruitObjSpace(Space):
    bgcolor = 0xFFFF00
    opcolor = 0xFFFF90
    images  = mnstrmap.Flappy.left
    hack    = 157

class FlowObjSpace(Space):
    bgcolor = 0xFF70FF
    opcolor = 0xFFC0FF
    images  = mnstrmap.Ghosty.left

# flash the __getitem__ a bit
# record operations somewhere on FlowObjSpace
# much slower!


# ____________________________________________________________

b = Board()
#h1 = HeadLine(bwidth//2, 80, "PyPy", 48, color=0xFF0000)
h2 = HeadLine(bwidth//2, 300, "PyPy", 160, color=0xCC1E2F)

sprmap['pypy'] = ('pypy.ppm', (0, 0, 149, 110))
Sprite((bwidth-149)//2, 100, sprget('pypy'))

#h3 = HeadLine(bwidth//2, 450, "          featuring", 32, color=0xCCCCCC)
b.pause('Press Space to continue and Left Arrow to go back')

for h in [h2]:
    h.gen.append(h.shiftcolor(0x400000, 4))
b.animate('', 0)

# ____________________________________________________________

def slide_nextline(line, pause=True, foreground=[]):
    global text
    for p in b.sprites[:]:
        if isinstance(p, Program):
            p.kill()
            for s in p.allspr:
                s.kill()
    text += line + '\n'
    p = Program(90, 250, text)
    for s in foreground:
        s.kill(); s.revive()
    b.animate('', 0)
    p.s.h += 8
    if pause:
        b.pause(' ')

def slide(title, lines):
    global b, text
    b = Board()
    h = Line(60, 120, title, 56, color=0x101010)
    h.gen.append(h.shiftcolor(0xFFBFDF, 3))
    b.animate('', 0)
    text = ''
    for line in lines:
        slide_nextline(line)


slide('PyPy Status Report',
      ['Highly compliant Python implementation in Python',
       'Quite complete',
       'Some original features already',
       'Program analysis/checking toolchain'])

# ____________________________________________________________

class Lemming(Sprite):
    def right(self, tox):
        self.setimages(self.cyclic([('lem-walk', 1, i) for i in range(8)], 1,
                                   doublesize))
        while self.x < tox:
            yield None
            self.step(4, 0)
    def down(self, toy):
        self.setimages(self.cyclic([('lem-fall', 1, i) for i in range(4)], 1,
                                   doublesize))
        while self.y < toy:
            yield None
            self.step(0, 8)
    def run(self):
        sprget(('lem-fall', 1, 0), doublesize)
        sprget(('lem-crash', 0), doublesize)
        for t in self.right(16+15*16-24):
            yield t
        for t in self.down(self.y+32):
            yield t
        for t in self.right(16+19*16-24):
            yield t
        for t in self.down(bheight - 80):
            yield t
        self.setimages(self.cyclic([('lem-crash', n) for n in range(16)], 1,
                                   doublesize))
        for n in range(17):
            yield None
        self.kill()
        yield "stop"

leftcol = 100

##b = Board()
##s = HeadLine(bwidth//2, 48, "Penty", 64, color=0x000000)
##s.gen.append(s.shiftcolor(0x0080FF, 4))
##slast = Sprite(leftcol, s.y-20, sprget(('lem-walk', 1, 0), doublesize))
##hwall(16, 384, 15)
##hwall(256, 384+32, 4)
##Lemming(192-64, 384-64)
##b.animate('+A Lemming in the role of the CPU: pretty dumb, follows path, crashes')

# ____________________________________________________________

class Nasty(Sprite):
    def left(self, tox):
        self.setimages(self.cyclic(mnstrmap.Nasty.left, 1, doublesize))
        while self.x > tox:
            yield None
            self.step(-9, 0)
    def right(self, tox):
        self.setimages(self.cyclic(mnstrmap.Nasty.right, 1, doublesize))
        while self.x < tox:
            yield None
            self.step(9, 0)
    def up(self, toy):
        while self.y > toy:
            self.step(0, -16)
            yield None
    def down(self, toy):
        while self.y < toy:
            self.step(0, 16)
            yield None
    def run(self):
        for t in self.right(300):
            yield t
        self.setimages(None)
        yield None
        self.seticon(sprget(mnstrmap.Nasty.left[1], doublesize))
        yield None
        yield None
        self.seticon(sprget(mnstrmap.Nasty.right[1], doublesize))
        yield None
        yield None
        self.seticon(sprget(mnstrmap.Nasty.left[2], doublesize))
        for t in self.up(384):
            yield t
        for t in self.left(136):
            yield t
        for t in self.down(bheight-80):
            yield t
        for t in self.left(16):
            yield t
        for t in self.right(100):
            yield t
        yield "stop"

##b = Board(last=slast)
##s = HeadLine(bwidth//2, 160, "CPy", 64, color=0x000000)
##s.gen.append(s.shiftcolor(0xA0A0A0, 4))
##slast = Sprite(leftcol, s.y-16, sprget(mnstrmap.Nasty.right[0], doublesize))
##hwall(192, 448, 24)
##Nasty(230, bheight-80)
##b.animate('+The regular CPython interpreter: an automaton, dumb too, more robust')

# ____________________________________________________________

##b = Board(last=slast)
##s = HeadLine(bwidth//2, 272, "The Abstracter", 48, color=0x000000)
##s.gen.append(s.shiftcolor(0xCC1E2F, 4))
##Sprite(leftcol, s.y-16, sprget(Player[0], doublesize))
##b.animate('+The Psyco guys, which we will introduce in due time...')

# ____________________________________________________________

##s = HeadLine(bwidth//2, 384, "The Bookkeeper", 48, color=0x000000)
##s.gen.append(s.shiftcolor(0xC8C8C8, 4))
##Sprite(leftcol, s.y-16, sprget(mnstrmap.Monky.right[0], doublesize))
##b.animate('+The Psyco guys, which we will introduce in due time...')

# ____________________________________________________________

##s = HeadLine(bwidth//2, 484, "The Codemaker", 48, color=0x000000)
##s.gen.append(s.shiftcolor(0xFF9933, 4))
##Sprite(leftcol, s.y-16, sprget(mnstrmap.Springy.right[0], doublesize))
##b.animate('+The Psyco guys, which we will introduce in due time...')

# ============================================================

b = Board()
p = Program(170, 50, """
def sum(seq):
    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total
""")
Sprite(p.s.x + p.s.w - 48 - 32, p.s.y + 7, sprget('py', doublesize))
b.pause('The Python code example we will use for the whole presentation')

# ____________________________________________________________

seq = [6,3,8,1,5]
states = [
    (1, {'seq': seq}),
    'pause+At the left, the "state" of the automaton keeps track of the local variables',
    (2, {'total': 0}),
    ]
total = 0
for i in range(len(seq)):
    states.append((3, {'i': i}))
    total += seq[i]
    states.append((4, {'total': total}))
states.append((5, {}))

r = RunCPython(40, 320, {'seq': seq}, 3, p, states)
b.animate('Here is how CPython interprets this code')

r.kill()

# ____________________________________________________________

seq = [6,3,8]

RED   = 0xC00000
GREEN = 0x008000

b = Board()
p = Program(170, 50, """
def sum(seq):
    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total
""")
space = StdObjSpace()
states = [
    'pause',
    (1, {'seq  ': '      '+str(seq)}),
    (2, {'total': '      0'}),
    (3, {'i    ': '      0'}),
    (3, {'item ': ''}),
    'pause',
    
    (3, {'seq  ': space.goto(0.9, 35),
         'i    ': space.goto(1.2, 35)}),
    (3, {}),
    (3, {}),
    (3, {}),
    (3, {}),
    (3, {'item ': space.compute(1)}),
    (3, {}),
    (3, {'item ': space.comefrom(1, 6, 25)}),
    (3, {}),
    (3, {}),
    (3, {}),
    (3, {}),
    (3, {}),
    (3, {}),
    'pause',

    (3, {'total': space.goto(-0.1, 35),
         'item ': space.goto(0.2, 35)}),
    (3, {}),
    (3, {}),
    (3, {}),
    (3, {'total': space.compute(0)}),
    (3, {}),
    (3, {'total': space.comefrom(0, 6, 25)}),
    (3, {}),
    (3, {}),
    (3, {}),
    (3, {}),
    (3, {}),
    (4, {}),
    'pause',

    #(2, {'total': 0}),
    ]
total = 0
for i in range(len(seq)):
    total += seq[i]
    if i>0:
        states.extend([
            (3, {'i    ': '      '+str(i)}),
            (3, {'seq  ': space.goto(0.9),
                 'i    ': space.goto(1.2)}),
            (3, {'item ': space.compute(1)}),
            (3, {'item ': space.comefrom(1, seq[i])}),
            (3, {}),
            (3, {}),
            (3, {}),

            (3, {'total': space.goto(-0.1),
                 'item ': space.goto(0.2)}),
            (3, {'total': space.compute(0)}),
            (3, {'total': space.comefrom(0, total)}),
            (3, {}),
            (4, {}),
            (4, {}),
        ])
states.append((5, {}))

r = RunCPython(40, 300, {'total': ''}, 4, p, states)

b.animate('')



# ____________________________________________________________

RED   = 0xC00000
GREEN = 0x008000

b = Board()
p = Program(170, 50, """
def sum(seq):
    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total
""")
space = FruitObjSpace()
states = [
    (1, {'seq  ': '      \x00594'}),
    (2, {'total': '      \x00596'}),
    (3, {'i    ': '      \x00597'}),
    (3, {'item ': ''}),
    'pause',
    
    (3, {'seq  ': space.goto(0.9),
         'i    ': space.goto(1.2)}),
    (3, {}),
    (3, {'item ': space.comefrom(1, '\x00598')}),
    (3, {}),
    (3, {}),
    #'pause',

    (3, {'total': space.goto(-0.1),
         'item ': space.goto(0.2)}),
    (3, {}),
    (3, {'total': space.comefrom(0, '\x00593')}),
    (3, {}),
    (4, {}),
    #'pause',

    (3, {'seq  ': space.goto(0.9),
         'i    ': space.goto(1.2)}),
    (3, {}),
    (3, {'item ': space.comefrom(1, '\x00602')}),
    (3, {}),
    (3, {}),
    #'pause',

    (3, {'total': space.goto(-0.1),
         'item ': space.goto(0.2)}),
    (3, {}),
    (3, {'total': space.comefrom(0, '\x00606')}),
    (3, {}),
    (4, {}),
    ]

states.append((5, {}))

r = RunCPython(40, 300, {'total': ''}, 4, p, states)

b.animate('')


# ____________________________________________________________

RED   = 0xC00000
GREEN = 0x008000

b = Board()
p = Program(40, 50, """
def sum(seq):
    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total
""")
space = FlowObjSpace()
states = [
    (1, {'seq  ': '      A'}),
    (2, {'total': '      B'}),
    (3, {'i    ': '      C'}),
    (3, {'item ': ''}),
    'pause',
    
    (3, {'seq  ': space.goto(0.9),
         'i    ': space.goto(1.2)}),
    (3, {}),
    (3, {'item ': space.comefrom(1, 'D')}),
    (3, {}),
    (3, {}),

    (3, {'total': space.goto(-0.1),
         'item ': space.goto(0.2)}),
    (3, {}),
    (3, {'total': space.comefrom(0, 'E')}),
    (3, {}),
    (4, {}),
    ]

r = RunCPython(40, 300, {'total': ''}, 4, p, states)

b.animate('')

p = Program(510, 140, "D = getitem(A, C)\nE = add(B, D)\n", bgcolor=0xFFFF7F)
b.pause(' ')

# ____________________________________________________________

##### * <=> translator.py: t.view()
b = Board()
b.pause(' ')
#####

slide("Staticness Conditions",
      ["do whatever you like at boot-time",
       "then no more dynamic function/class creation",
       "constant globals, constant class attr/methods",
       "can use exceptions",
       "type coherency"])

slide("Type Coherency",
      ['a "type" means here a "set of objects"',
       "customizable for your program",
       'for PyPy, we implemented a reasonable selection'])

##### * <=> t.annotate()
b = Board()
b.pause(' ')
#####

slide("Algorithm",
      ['"naive" forward propagation',
       'also known as "abstract interpretation"',
       'bottom-up fixpoint search',
       'user provides an entry point function'])

slide("Features",
      ["analyses the preinitialized program in-memory",
       "no user annotation",
       "full-program analysis"])

s1 = Sprite(364, 333, sprget(691))   # sugar
b.pause(' ')

s2 = Sprite(364, 294, sprget(618))   # red diamond
b.pause(' ')

s3 = Sprite(364-32+3, 196, sprget(16))   # big violet diamond
b.pause(' ')

slide_nextline("mostly language-independent", False, [s1,s2,s3])
Sprite(450, 400-8, sprget(593))
Sprite(470, 396-8, sprget(596))
Sprite(482, 402-8, sprget(606))
Sprite(530, 397, sprget(595))
Sprite(512, 400, sprget(594))
b.pause(' ')

# ____________________________________________________________

slide("Compare To",
      ["@types(int, str, returning=int)     "])

s = Sprite(480, 246, sprget(618))
n = Sprite(bwidth-8*15, 246, sprget(mnstrmap.Monky.left[-1]))
n.setimages(n.cyclic(mnstrmap.Monky.left, 1))
n.gen.append(n.walkabit(20-8, -15, 0))
b.animate('', 0)
s.kill()
n.setimages(n.cyclic(mnstrmap.Monky.right, 1))
n.gen.append(n.walkabit(20, +15, 0))
b.animate('')
n.kill()

slide_nextline("exact restriction-less typing (local vars only)     ", False)
s1 = Sprite(660,    296, sprget(618))
s2 = Sprite(660+32, 296, sprget(619))
b.pause(' ')

slide_nextline("full-program source code analysis (Starkiller)", False, [s1,s2])
s3 = Sprite(660+16, 333, sprget(630))   # sugar
b.pause(' ')

# ____________________________________________________________

slide("Related Tools", [])
slide_nextline("Python2C", False)
slide_nextline("Pyrex (Python-like source with types)", False)
slide_nextline("Psyco (100% run-time)")

# ____________________________________________________________

slide("PyPy's Type Model",
      ["int, float, str, bool, function",
       "tuple, list, dict, iter",
       "prebuilt constants",
       "class, instance"])

##### * <=> t.annotate() with OO  (translate_pypy1.py?)
b = Board()
b.pause(' ')
#####

slide("Code Generation",
      ["can generate Pyrex (at PyCon 2004 already)",
       "can generate a slow C extension module (a la Python2C)",
       "can do Common Lisp / Java / LLVM / C++ / Python..."])

slide("Next Steps",
      ["good C code",
       "Java? maybe, for object model",
       "LLVM in development (Carl Friedrich Bolz)"])

slide("Conclusion",
      ["   PyPy CPython-compliancy: OK   ",
       " PyPy running over CPython: nice but too slow",
       "    type inferencing tools: OK",
       "infer types in PyPy source: OK"])
slide_nextline(
       "  generate fast typed code: next step!", False)

for x, images in [(0,   mnstrmap.Monky.right),
                  (-64, mnstrmap.Nasty.right),
                  (-128, mnstrmap.Orcy.right)]:
    n = Sprite(x, bheight-32-16, sprget(images[-1]))
    n.setimages(n.cyclic(images, 1))
    n.gen.append(n.walkabit((bwidth+192)//15, +15, 0))
b.animate('')

