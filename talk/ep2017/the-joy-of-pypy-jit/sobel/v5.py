import array
from math import sqrt
from v2 import Image
from pypytools.codegen import Code

def Kernel(matrix):
    height = len(matrix)
    width = len(matrix[0])
    code = Code()
    with code.block('def apply(img, x, y):'):
        code.w('value = 0.0')
        for j, row in enumerate(matrix, -(height/2)):
            for i, k in enumerate(row, -(width/2)):
                if k == 0:
                    continue
                code.w('value += img[x+{i}, y+{j}] * {k}', i=i, j=j, k=k)
        code.w('return value')
    #
    code.compile()
    return code['apply']

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
