from subprocess import Popen, PIPE, STDOUT
import os, re
from image import Image
from array import array

def mplayer(filename='tv://', options=()):
    cmd = Popen(['mplayer', '-vo', 'null', '-ao', 'null',
                 '-frames', '1'] + list(options) + [filename],
                stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (out, err) = cmd.communicate()
    for line in (out + err).split('\n'):
        m = re.search('(VIDEO|VO): .*? (\d+)x(\d+)', line)
        if m:
            width, height = int(m.group(2)), int(m.group(3))
            break
    else:
        raise IOError
    fmt = 'y8'

    mplayer = Popen(['mencoder', '-o', '-',
                                 '-ovc', 'raw', '-of', 'rawvideo',
                                 '-vf', 'format=' + fmt,
                                 '-nosound', '-really-quiet',
                    ] + list(options) + [filename],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        try:
            data = array('B')
            data.fromfile(mplayer.stdout, width*height)
            img = Image(width, height, 'B', data)
        except EOFError:
            raise StopIteration
        yield img

        

class MplayerViewer(object):
    def __init__(self):
        self.width = self.height = None

    def view(self, img):
        if img.data.typecode != 'B':
            out = img.new(typecode='B')
            for y in xrange(img.height):
                for x in xrange(img.width):
                    out[x, y] = int(min(max(img[x, y], 0), 255))
            img = out
        if not self.width:
            w, h = img.width, img.height
            self.mplayer = Popen(['mplayer', '-', '-benchmark',
                                  '-demuxer', 'rawvideo',
                                 '-rawvideo', 'w=%d:h=%d:format=y8' % (w, h),
                                 '-really-quiet'],
                                 stdin=PIPE, stdout=PIPE, stderr=PIPE)
            
            self.width = img.width
            self.height = img.height
        assert self.width == img.width
        assert self.height == img.height
        img.data.tofile(self.mplayer.stdin)

    def viewsc(self, img):
        a, b = min(img), max(img)
        if a == b:
            b += 1
        self.view((img - a) * 255 / (b - a))

viewers = {}
def view(img, name='default', scale=False):
    try:
        viewer = viewers[name]
    except KeyError:
        viewer = viewers[name] = MplayerViewer()
    if scale:
        viewer.viewsc(img)
    else:
        viewer.view(img)

def viewsc(img, name='default'):
    view(img, name, True)


