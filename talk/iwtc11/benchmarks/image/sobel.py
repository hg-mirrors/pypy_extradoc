from noborder import NoBorderImagePadded
from math import sqrt

def sobeldx(img):
    res = img.clone(typecode='d')
    for p in img.pixeliter():
        res[p] = (-1.0 * img[p + (-1,-1)] + 1.0 * img[p + (1,-1)] + \
                  -2.0 * img[p + (-1, 0)] + 2.0 * img[p + (1, 0)] + \
                  -1.0 * img[p + (-1, 1)] + 1.0 * img[p + (1, 1)]) / 4.0
    return res

def sobeldy(img):
    res = img.clone(typecode='d')
    for p in img.pixeliter():
        res[p] = (-1.0*img[p + (-1,-1)] -2.0*img[p + (0,-1)] -1.0*img[p + (1,-1)] + \
                   1.0*img[p + (-1, 1)] +2.0*img[p + (0, 1)] +2.0*img[p + (1, 1)]) / 4.0
    return res

def sobel_magnitude(img):
    res = img.clone(typecode='d')
    for p in img.pixeliter():
        dx = -1.0 * img[p + (-1,-1)] + 1.0 * img[p + (1,-1)] + \
             -2.0 * img[p + (-1, 0)] + 2.0 * img[p + (1, 0)] + \
             -1.0 * img[p + (-1, 1)] + 1.0 * img[p + (1, 1)]
        dy = -1.0*img[p + (-1,-1)] -2.0*img[p + (0,-1)] -1.0*img[p + (1,-1)] + \
              1.0*img[p + (-1, 1)] +2.0*img[p + (0, 1)] +2.0*img[p + (1, 1)]
        res[p] = sqrt(dx**2 + dy**2) / 4.0
    return res

def uint8(img):
    res = img.clone(typecode='B')
    for p in img.pixeliter():
        res[p] = min(max(int(img[p]), 0), 255)
    return res

if __name__ == '__main__':
    from io import mplayer, view
    import sys
    from time import time

    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = 'test.avi'

    try:
        import pypyjit
        pypyjit.set_param(trace_limit=200000)
    except ImportError:
        pass

    start = time()
    for fcnt, img in enumerate(mplayer(NoBorderImagePadded, fn)):
        #view(img)
        #sobeldx(img)
        view(uint8(sobel_magnitude(img)))
        print 1.0 / (time() - start), 'fps'
        start = time()
