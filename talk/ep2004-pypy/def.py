
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
h2 = HeadLine(bwidth//2, 200, "PyPy", 160, color=0xCC1E2F)
#h3 = HeadLine(bwidth//2, 450, "          featuring", 32, color=0xCCCCCC)
b.pause('Press Space to continue and Left Arrow to go back')

for h in [h2]:
    h.gen.append(h.shiftcolor(0x400000, 4))
b.animate('', 0)

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
    (1, {'seq  ': '      ?'}),
    (2, {'total': '      ?'}),
    (3, {'i    ': '      \x00597'}),  XXX
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
# ____________________________________________________________


raise SystemExit


states = [
    (1, {'seq': 'an object'}),
    "pause We can do it step by step:\nat this point seq is some object and total is zero...",
    (2, {'total': 0}),
    "pause But let's consider the case where seq is a list,\notherwise we don't know what the len() could possibly do",
    (2, {'seq': (RED, 'a list')}),
    "pause So let's say that seq is a list and have a look inside the loop",
    (3, {'i': 'an integer'}),
    'pause seq[i] means read the ith item of that list',
    (3, {'seq[i]': 'an object'}),
    "pause To understand what += does let's assume that this item is an int",
    (3, {'seq[i]': (RED, 'an integer')}),
    'pause So += adds 0 and this int, and returns this int',
    (4, {'total': 'an integer'}),
    "pause Then, the second time through the loop, here's what will occur...",
    (3, {'seq[i]': None}),
    'pause seq[i] will read the ith list item',
    (3, {'seq[i]': 'an object'}),
    'pause which we assume is still an int',
    (3, {'seq[i]': (RED, 'an integer')}),
    'pause so that we add it to the int stored in total',
    (4, {'total': 'an integer'}),
    'pause and so on and so forth for the next iterations',
    (3, {'seq[i]': None}),
    ]
r = RunPsyco(40, 32, {'seq[i]': 'an integer'}, 4, p, states)
b.animate("But we're more clever than CPython: we can reason about\nthis piece of code to understand how it works more generally")

r.kill()

# ____________________________________________________________

log = Bookkeeper(40, 299, 'list, int, int')

states = [
    "pause IOW we have a memory too -- let's introduce the Bookkeeper\nwhich keeps a log of what states have already been seen",
    (1, {'seq': 'an object'}),
    (2, {'total': 0}),
    (2, {'seq': (RED, 'a list')}),
    (3, {'i': 'an integer',               log: (GREEN, 'list, 0, int')}),
    'pause The second time we enter the loop, the state is different',
    (3, {'seq[i]': 'an object'}),
    (3, {'seq[i]': (RED, 'an integer')}),
    (4, {'total': 'an integer'}),
    (3, {'seq[i]': None,                  log: (GREEN, 'list, int, int')}),
    'pause The third time the state is identical:\nwe remember we have already seen and understood this case',
    (3, {'seq[i]': 'an object'}),
    (3, {'seq[i]': (RED, 'an integer')}),
    (4, {'total': 'an integer'}),
    (3, {'seq[i]': None,                  log: (GREEN, 'list, int, int')}),
    ]
r = RunPsyco(40, 32, {'seq[i]': 'an integer'}, 4, p, states)
b.animate("We are more intelligent than CPython both because we can reason\nand because we realize that after the 2nd iteration it will always be the same")

r.kill()
log.kill()

# ____________________________________________________________
# Without check()

log = Bookkeeper(40, 299, 'list, int, int')
code = Codemaker(log.x + log.w + 28, 299, 'jump back to Label')

states = [
    'pause Up to this point, boilerplate only.\nThe real operations start now',
    (1, {'seq': 'an object'}),
    (2, {'total': 0}),
    (2, {'seq': (RED, 'a list'),          }),
    (3, {'i': 'an integer',        log: (GREEN, 'list, 0, int')}),
    'pause',
    (3, {'seq[i]': 'an object',    log: '', code: '  read list item'}),
    'pause',
    (3, {'seq[i]': (RED, 'an integer'),   }),
    (4, {'total': 'an integer',    log: '', code: '  add 0 -- no op'}),
    "pause Let the Bookkeeper also track positions in the Codemaker's log",
    (3, {'seq[i]': None,           log: (GREEN, 'list, int, int'),
                                   code: (GREEN, 'Label:')}),
    'pause Note how the recorded operations are quite low-level\nand created step by step by following the source as if interpreting it',
    (3, {'seq[i]': 'an object',    log: '', code: '  read list item'}),
    (3, {'seq[i]': (RED, 'an integer'),   }),
    (4, {'total': 'an integer',    log: '', code: '  add two ints'}),
    'pause Already seen.  We write a jump in the Codemaker log to mean\n"from now on, it is just the same as before"\nNote how it starts to look like a low-level version of the source',
    (3, {'seq[i]': None,           log: (GREEN, 'list, int, int'),
                                   code: (GREEN, 'jump back to Label')}),
    ]
r = RunPsyco(40, 32, {'seq[i]': 'an integer'}, 4, p, states)
b.animate("We introduce the Codemaker to track what we\nhave understood about each case: what each case really does")

r.kill()
log.kill()
code.kill()

# ____________________________________________________________
# With check()

COMPRESSED = 1

log = Bookkeeper(40, 299, '  seq[i] is an integer')
code = Codemaker(log.x + log.w + 28, 299, '  read list item')

states = [
    (1, {'seq': 'an object'}),
    (2, {'total': 0}),
    "pause This assumption must be checked\nwhen the function is actually called",
    (2, {'seq': (RED, 'a list'),   log: (RED, '  seq is a list'),
                                   code: (RED, '  check(list)')}),
    'pause Similarily, we must check that the\nlist item we read here is really an int',
    (3, {'i': 'an integer',        log: (GREEN, 'list, 0, int'),
                                   code: (GREEN, 'L1:')}),
    (3, {'seq[i]': 'an object',    log: '', code: '  read list item'}),
    (3, {'seq[i]': (RED, 'an integer'), log: (RED, '  seq[i] is an integer'),
                                   code: (RED, '  check(int)')}),
    'pause',
    (4, {'total': 'an integer'}),
    (3, {'seq[i]': None,           log: (GREEN, 'list, int, int'),
                                   code: (GREEN, 'L2:')}),
    (3, {'seq[i]': 'an object',    log: '', code: '  read list item'}),
    (3, {'seq[i]': (RED, 'an integer'), log: (RED, '  seq[i] is an integer'),
                                   code: (RED, '  check(int)')}),
    'pause The resulting Codemaker log is now safer low-level code',
    (4, {'total': 'an integer',    log: '', code: '  add two ints'}),
    (3, {'seq[i]': None,           log: (GREEN, 'list, int, int'),
                                   code: (GREEN, 'jump back to L2')}),
    ]
r = RunPsyco(40, 32, {'seq[i]': 'an integer'}, 4, p, states)
b.animate("Let's start over again and consider that we assumed\nat this point that seq was a list")

# ____________________________________________________________

b = Board()
p = Program(370, 43, """
def sum(seq):
    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total
""")

log = Bookkeeper(40, 299+8, '  seq[i] is an int')
code = Codemaker(log.x + log.w + 28, 299-20, '  check(type(item)==int)',
                 nblines=10)

states = [
    (1, {'seq': 'an object'}),
    (2, {'total': 0}),
    (2, {'seq': (RED, 'a list object'), log: (RED, '  seq is a list'),
                                   code: (RED, '  check(type(seq)==list)')}),
    "pause The list seq contains int objects\ni.e. whole structures with type pointer and refcount",
    (3, {'i': 'an integer',        log: (GREEN, 'list, 0, int'),
                                   code: (GREEN, 'L1:')}),
    (3, {'item': 'an object',      log: '', code: '  item = seq[i]'}),
    (3, {'item': (RED, 'an int object'),
                                   log: (RED, '  item is an int'),
                                   code: (RED, '  check(type(item)==int)')}),
    'pause Operations like 0+item involve fetching\nthe int value out of the PyIntObject structure that item points to',
    (4, {'total': 'an integer',    log: '', code: '  total = 0+intval(item)'}),
    "pause Note that total is just an integer\nbecause no one is interested in having a full heap structure for it",
    (3, {'item': None,             log: (GREEN, 'list, int, int'),
                                   code: (GREEN, 'L2:')}),
    (3, {'item': 'an object',      log: '', code: '  item = seq[i]'}),
    (3, {'item': (RED, 'an int object'),
                                   log: (RED, '  item is an int'),
                                   code: (RED, '  check(type(item)==int)')}),
    'pause+unlike all items, which come as full structures out of the list',
    (4, {'total': 'an integer',    log: '', code: '  total += intval(item)'}),
    (3, {'item': None,             log: (GREEN, 'list, int, int'),
                                   code: (GREEN, 'jump back to L2')}),
    ]
r = RunPsyco(40, 32, {'item': 'an int object'}, 4, p, states)
b.animate("In C there are two kinds of integers: the int variables,\nand PyIntObject structures in the heap standing for a Python object of type int")

# ============================================================

b = Board()
code.revive(dx = -20 - code.x, dy = -120)
b.animate(' ', 0)

c = CPU(code.x + code.w + 28, code.y, ' check(item->ob_type==Int_Type);',
        nblines=10)
c.append((RED, ' check(seq->ob_type==List_Type);'))
c.append(      'Label1:')
c.append(      ' PyObject*item=List_Item(seq,i);')
c.append((RED, ' check(item->ob_type==Int_Type);'))
c.append(      ' int total = 0 + item->ob_ival;')
c.append(      'Label2:')
c.append(      ' PyObject*item=List_Item(seq,i);')
c.append((RED, ' check(item->ob_type==Int_Type);'))
c.append(      ' total += item->ob_ival;')
c.append(      'goto Label2;')
b.pause("Now the result is really like low-level C code that performs the same job\n(though still missing a few instructions about i and breaking out of the loop)")

# ============================================================

b = Board()
p = Program(400, 43, """
def sum(seq):
    L = len(seq)
    Rng = range(L)
    Iter = iter(Rng)
    for i in Iter:
""")

log = Bookkeeper(40, 299, 'list, range(L), iter(Rng)')
code = Codemaker(log.x + log.w + 28, 299, '  check(type(seq)==list)')

states = [
    (1, {'seq': 'an object'}),
    'pause The len() forces us to consider the case where seq is a list;\nthen L is an int that can be read easily out of the list structure',
    (1, {'seq': (RED, 'a list object'),
                                   log: (RED, '  seq is a list'),
                                   code: (RED, '  check(type(seq)==list)')}),
    (2, {'L': 'an integer',        log: '', code: '  L = list_len(seq)'}),
    'pause range(L) produces a new list, which humans will consider as\n"the list of all ints from 0 to L-1"\ninstead of memorizing an explicit "[0,1,2,3,4,5,6,7,8,9]"',
    (3, {'Rng': 'the range(0, L)', 'L': None}),
    'pause Similarily, we think about Iter as an iterator over Rng\nbut its current position is a detail that we expect to change all the time,\nso we just store it into some variable initialized to 0',
    (4, {'Iter': 'an iter for Rng', log: '', code: '  Iter.pos = 0'}),
    'pause The Bookkeeper (i.e. our memory)\nnow has a more complex state to remember',
    (4, {                          log: (GREEN, 'list, range(L), iter(Rng)'),
                                   code: (GREEN, 'L1:')}),
    'pause Here are the operations done to enter the loop\nThe check is: would reading the Iter.pos-th element of Rng raise an IndexError?',
    (4, {                          log: (RED, '  IndexError?'),
                                   code: (RED, '  check(Rng[Iter.pos])')}),
    (4, {'i': 'an integer', log: '', code: '  i = Rng[Iter.pos]'}),
    (4, {             log: '',     code: '  Iter.pos += 1'}),
    'pause i is an integer because Rng is a range, in particular a list of integers\nAfter the body of the loop we jump back because the state is the same one',
    (5, {             log: '',     code: '  ...'}),
    (4, {                          log: (GREEN, 'list, range(L), iter(Rng)'),
                                   code: (GREEN, 'jump back to L1')}),
    ]
r = RunPsyco(40, 32, {'Iter': 'an iter for Rng'}, 4, p, states)
r.st.liney0 = 18
b.animate('Remember how for loops work in Python:\nhere is a detailled equivalent version')

# ============================================================

b = Board()
code.revive(dx = -20 - code.x, dy = -120)
b.animate(' ', 0)

c = CPU(code.x + code.w + 28, code.y, ' check(item->ob_type==Int_Type);',
        nblines=9)
c.append((RED, ' check(seq->ob_type==List_Type);'))
c.append(      ' int L = List_Size(seq);')
c.append(      ' int Iter_pos = 0;')
c.append(      'Label1:')
c.append((RED, ' check(Iter_pos < L);'))
c.append(      ' int i = 0 + Iter_pos;')
c.append(      ' ++Iter_pos;')
c.append(      ' ...')
c.append(      'goto Label1;')
b.pause('Corresponding low-level C code: because we know what Rng is,\nwe can provide efficient equivalents of Rng[Iter.pos]\nusing explicitely the start 0 of the range, and its length L\nNote that the check(Iter_pos < L) fails at the end of the loop')

# ============================================================

b = Board()
p = Program(370, 43, """
def sum(seq):
    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total
""")

log = Bookkeeper(40, 299, '  got IndexError')
code = Codemaker(log.x + log.w + 28, 299, '  total = newint(total)')

states = [
    (4, {'total': 'an integer',    log: (RED, '  got IndexError'),
                                   code: (RED, '# IndexError')}),
    'pause for jumps here after the StopIteration. return turns total --\nwhich was an int -- into a complete int object to send back to the caller',
    (5, {'total': 'an int object', log: '',
                                   code: 'total = newint(total)'}),
    (5, {                          log: '',
                                   code: 'return total'}),
    ]
r = RunPsyco(40, 32, {'total': 'an int object'}, 3, p, states)
b.animate('If this check fails it means that we got an IndexError\nwhich is turned into a StopIteration, and silenced out by the for loop\nNo code is needed to create and immediately eat exceptions')

# ============================================================

b = Board()
code.revive(dx = -20 - code.x, dy = -120)
b.animate(' ', 0)

c = CPU(code.x + code.w + 28, code.y, ' PyObject*total=Int_From(total);',
        nblines=9)
c.append((RED,  ' // got IndexError'))
c.append(       ' PyObject*total=Int_From(total);')
c.append(      ' return total;')
b.pause('The C equivalent...')

# ============================================================

b = Board()
p = Program(400, 43, """
def sum(seq):
    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total
""")
b.pause("Let's summarize...")

# ____________________________________________________________

def populateit(c, brk, extra):
    global line_hack
    if brk == 1:
        c.append((RED,'  what is type(seq)?'))
        return
    c.append((RED,   '  check(type(seq) == list)'))
    c.append(        '  L = list_len(seq)')
    c.append(        '  Iter.pos = 0')
    c.append((GREEN, 'L1:'))
    c.append((RED,   '  check(Iter.pos < L)'))
    c.append(        '  i = 0 + Iter.pos')
    c.append(        '  Iter.pos += 1')
    c.append(        '  item = seq[i]')
    if brk == 9:
        c.append((RED,'  what is type(item)?'))
        return
    c.append((RED,   '  check(type(item) == int)'))
    c.append(        '  total = 0 + intval(item)')
    c.append((GREEN, 'L2:'))
    c.append((RED,   '  check(Iter.pos < L)' + extra))
    c.append(        '  i = 0 + Iter.pos')
    c.append(        '  Iter.pos += 1')
    c.append(        '  item = seq[i]')
    if brk == 16:
        c.append((RED,'  what is type(item)?'))
        return
    c.append((RED,   '  check(type(item) == int)'))
    line_hack = b.sprites[-1]
    c.append(        '  total = total + intval(item)')
    c.append((GREEN, 'goto L2'))

def writeit(brk = 18, extra = '', cls=Codemaker, cls1=Codemaker):
    global last_args, last_c
    last_args = brk, extra
    del b.sprites[:]
    if not extra:
        cls1 = cls
    c = cls1(10, 37, '  check(Iter.pos < L) else goto L3', nblines=brk)
    populateit(c, brk, extra)
    last_c = c
    if extra:
        c = extracodeblock(cls)
    lastline = b.sprites[-1]
    myside = cls is Codemaker
    opposite_s[myside] = c.s
    otherside = not myside
    if otherside in opposite_s:
        opposite_s[otherside].revive()
    return c, lastline

def lem_runto(y=None, steps=None, cut=0, x=None, cls1=Codemaker):
    global lem_y
    c, lastline = writeit(*last_args, **{'cls': CPU_Right, 'cls1': cls1})
    lem = c.s
    del lem.gen[:]
    if y is None:
        y = lem.y
        if last_args[1]:   # extra
            y += 24
    lem.y = lem_y
    lem.setimages(lem.cyclic([('lem-walk', -1, i) for i in range(8)], 1,
                             doublesize))
    if steps is None:
        steps = (abs(y-lem.y) // 6) or 1
    lem.gen.append(lem.straightline(x or lem.x, y, steps))
    if cut:
        steps -= cut
    lem.gen.append(lem.stopafter(steps+1))
    lem_y = y

def extracodeblock(cls):
    if cls is Codemaker:
        cls = DarkerCodemaker
    c = cls(410, 400, ' total = Int_From(total)', nblines=3)
    c.append((GREEN, 'L3:'))
    c.append(        '  total = Int_From(total)')
    c.append(        '  return total')
    return c

def flash(ntext):
    del b.sprites[:]
    c, line = writeit(*last_args)
    line2 = Line(line.x, line.y, line.text, line.size, line.bold,
                 line.font, line.color)
    line.color = Codemaker.bgcolor
    line.text = ntext
    line.gen.append(line.shiftcolor(line2.color, 4, 5))
    line2.gen.append(line2.shiftcolor(line.color, 4))
    line2.gen.append(line2.die(5))
    b.animate(' ', 0)

#writeit()
#b.pause(' ')

opposite_s = {}

writeit(extra=' else goto L3')
p = Program(400, 43, """
def sum(seq):
    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total
""")
b.pause('This is what the Codemaker produces for this function')

# ============================================================

b = Board()
writeit(brk=1)
b.pause("Now let's see the dynamic aspect:\nhow would Psyco know in the first place that seq is a list of integers?\nWhen len(seq) is first found, we know nothing about seq\nso we don't know what len(seq) means.\nWe cannot write check(type(seq) == list) right now,\nwe have to ask what type(seq) will be in practice.")

# ____________________________________________________________

lem_y = -64
lem_runto()
b.animate('Then we stop the analysis and let the processor run\nthe C equivalent of this code\nuntil the processor reaches the question -- which is translated as\nthe instruction "send this value back to Psyco"')

# ____________________________________________________________

flash('  check(type(seq) == list)')
writeit(brk=9)
b.pause('The processor sends the answer "list" back to Psyco\nWe can replace the question with the check, and proceed with our analysis\nuntil we are stuck again because we don\'t know the type of item')

# ____________________________________________________________

lem_runto()
b.animate('+Let the processor progress a bit')

# ____________________________________________________________

flash('  check(type(item) == int)')
writeit(brk=16)
b.pause('The processor sends the answer "int"\nWe replace the question with the check, and proceed with our analysis')

# ____________________________________________________________

lem_runto()
b.animate('Answer: "int"')

# ____________________________________________________________

flash('  check(type(item) == int)')
writeit()
b.pause('And now we are done because we have already seen this state')

# ____________________________________________________________

msg = '+The processor can go on, this time uninterrupted'
opposite_s.clear()
lem_runto();                b.animate(msg, 0)
top = 300
bottom = lem_y
lem_runto(top, 4);          b.animate(msg, 0)
lem_runto(bottom, cut=20);  b.animate(msg, 0)
lem_runto(top, 4);          b.animate(msg, 0)
lem_runto(bottom, cut=20);  b.animate(msg, 0)
lem_runto(top, 4);          b.animate(msg, 0)
lem_runto(bottom, cut=20);  b.animate(msg, 0)
lem_runto(top, 4);          b.animate(msg, 0)
lem_runto(335)
b.animate('Until this check fails')

# ____________________________________________________________

last_c2, ignored = writeit(extra=' else goto L3')
b.pause('At this time only, we analyse what occurs when this check fails\nand let the processor continue')

# ____________________________________________________________

opposite_s.clear()
lem_runto()
b.animate('The code is complete for the next time the function is called with a list\nof ints. The processor will be able to run the whole function uninterrupted')

# ____________________________________________________________

lem_runto(x=350, cls1=CPU_Nowhere)
b.animate("If the function is later called with a list containing a float\nthis check will fail")
last_c2, ignored = writeit(extra=' else L3')

# ============================================================

b = Board()
p = Program(370, 43, """
def sum(seq):
    total = 0
    for i in range(len(seq)):
        total += seq[i]
    return total
""")

log = Bookkeeper(40, 299+14, '  seq[i] is a float')
code = Codemaker(log.x + log.w + 28, 299-44, '  total = total+floatval(item)',
                 nblines=11)
code.bgcolor = 0xC0C058

states = [
    (3, {'seq': 'a list object',   code: (GREEN, 'L4:')}),
    (3, {'total': 'an integer'}),
    (3, {'i': 'an integer'}),
    'pause This time we assume that item is a float and proceed',
    (3, {'item': (RED, 'a float object'),
                                   log: (RED, '  item is a float'),
                                   code: (RED, '  check(type(item)==float)')}),
    'pause int+float gives us a float for total',
    (4, {'total': 'a float',      log: '',
                                   code: '  total = total+floatval(item)'}),
    'pause The loop starts with a state we have never seen',
    (2, {'item': None,             log: (GREEN, 'list, float, int'),
                                   code: (GREEN, 'L5:')}),
    'pause+So we continue the analysis',
    (2, { log: (RED, 'IndexError?'), code: (RED,   '  check(Iter.pos < L)')}),
    (2, { log: '',                   code: '  i = 0 + Iter.pos'}),
    (2, { log: '',                   code: '  Iter.pos += 1'}),
    (3, {'item': 'an object',      log: '', code: '  item = seq[i]'}),
    (3, {'item': (RED, 'a float object'),
                                   log: (RED, '  item is a float'),
                                   code: (RED, '  check(type(item)==float)')}),
    (4, {'total': 'a float',      log: '', code: '  total += floatval(item)'}),
    'pause This time we have already seen this state, so we are done',
    (2, {'item': None,             log: (GREEN, 'list, float, int'),
                                   code: (GREEN, 'jump back to L5')}),
    ]
r = RunPsyco(40, 32, {'item': 'a float object'}, 4, p, states)
b.animate('+We resume the analysis at the failed check point')

# ============================================================

b = Board()
last_c.revive(dx = 0, dy = -300)
last_c2.revive(dx = +25, dy = -345)
code.revive(dx = -60, dy = 0)
b.animate(' ', 0)

def flash2():
    line = line_hack
    line2 = Line(line.x, line.y, line.text, line.size, line.bold,
                 line.font, line.color)
    line.color = Codemaker.bgcolor
    line.text += ' else L4'
    line.gen.append(line.shiftcolor(line2.color, 4, 5))
    line2.gen.append(line2.shiftcolor(line.color, 4))
    line2.gen.append(line2.die(5))
    b.animate('The block is linked from the failing check and the result is a larger version\nof the function capable of adding lists of ints and floats, efficiently')

flash2()

# ============================================================

b = Board()
h1 = HeadLine(bwidth//2, 300, "The End", 48, color=0x400000)
h1.gen.append(h1.shiftcolor(0xCC1E2F, 6))
b.animate(' ')
