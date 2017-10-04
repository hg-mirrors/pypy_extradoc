import array
from math import sqrt
from v3 import Image
from pypytools.codegen import Code

def Kernel(matrix):
    height = len(matrix)
    width = len(matrix[0])
    code = Code()
    with code.block('def apply(img, p):'):
        code.w('value = 0.0')
        for j, row in enumerate(matrix, -(height/2)):
            for i, k in enumerate(row, -(width/2)):
                if k == 0:
                    continue
                code.w('value += img[p+{delta}] * {k}', delta=(i, j), k=k)
        code.w('return value')
    #
    code.compile()
    return code['apply']


def sobel(img):
    """
    Like v4, but unrolling the Kernel loop
    """
    img = Image(*img)
    out = Image(img.width, img.height)
    for p in img.noborder():
        Gx = Kernel([[-1.0, 0.0, +1.0],
                     [-2.0, 0.0, +2.0],
                     [-1.0, 0.0, +1.0]])

        Gy = Kernel([[-1.0, -2.0, -1.0],
                     [0.0,  0.0,  0.0],
                     [+1.0, +2.0, +1.0]])

        dx = Gx(img, p)
        dy = Gy(img, p)
        value = min(int(sqrt(dx*dx + dy*dy) / 2.0), 255)
        out[p] = value
    return out
