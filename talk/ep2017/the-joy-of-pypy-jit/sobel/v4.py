import array
from math import sqrt
from v2 import Image

class Kernel(object):

    def __init__(self, matrix):
        self.height = len(matrix)
        self.width = len(matrix[0])
        self.matrix = matrix

    def __call__(self, img, x, y):
        value = 0.0
        for j, row in enumerate(self.matrix, -(self.height/2)):
            for i, k in enumerate(row, -(self.width/2)):
                value += img[x+i, y+j] * k
        return value


Gx = Kernel([[-1.0, 0.0, +1.0],
             [-2.0, 0.0, +2.0],
             [-1.0, 0.0, +1.0]])

Gy = Kernel([[-1.0, -2.0, -1.0],
             [0.0,  0.0,  0.0],
             [+1.0, +2.0, +1.0]])

def sobel(img):
    """
    Like v3, but with a generic Kernel class
    """
    img = Image(*img)
    out = Image(img.width, img.height)
    for y in xrange(1, img.height-1):
        for x in xrange(1, img.width-1):
            dx = Gx(img, x, y)
            dy = Gy(img, x, y)
            value = min(int(sqrt(dx*dx + dy*dy) / 2.0), 255)
            out[x, y] = value
    return out
