.. include:: beamerdefs.txt

==========================================
The joy of PyPy JIT: abstractions for free
==========================================

About me
---------

- PyPy core dev

- ``pdb++``, ``cffi``, ``vmprof``, ``capnpy``, ...

- @antocuni

- http://antocuni.eu


General question
----------------

Q: "How fast is PyPy?"

|pause|

A: "It depends"


speed.pypy.org
---------------

.. image:: speed.png
   :scale: 40%
           

The joy of PyPy
----------------

- No single "speedup" factor

- The better the code, the greater the speedup

           
Good code
---------

- Correct

- Readable

- Easy to maintain

- Nice APIs

- Fast


Abstractions
------------

- functions

- classes

- inheritance

- etc.

- PRO: readability
  
- CON: speed?

  
Example: Sobel filter
----------------------

Edge detection
|br|
   
.. image:: sobel.png
       :scale: 40%


Image
-----

- greyscale

- `w`, `h`

- `array.array('B')` of `w * h` bytes

- pixel `(x, y)` at index `x + w*y`


Version 0
---------

|scriptsize|

.. sourcecode:: python

    def sobel(img):
        w, h, data = img
        data_out = array.array('B', [0]) * (w*h)
        out = w, h, data_out
        for y in xrange(1, h-1):
            for x in xrange(1, w-1):
                dx = (-1.0 * data[(x-1) + w*(y-1)] +
                       1.0 * data[(x+1) + w*(y-1)] +
                      -2.0 * data[(x-1) + w*y    ] +
                       2.0 * data[(x+1) + w*y    ] +
                      -1.0 * data[(x-1) + w*(y+1)] +
                       1.0 * data[(x+1) + w*(y+1)])
 
                dy = (-1.0 * data[(x-1) + w*(y-1)] +
                      -2.0 * data[x     + w*(y-1)] +
                      -1.0 * data[(x+1) + w*(y-1)] +
                       1.0 * data[(x-1) + w*(y+1)] +
                       2.0 * data[x     + w*(y+1)] +
                       1.0 * data[(x+1) + w*(y+1)])
 
                value = min(int(sqrt(dx*dx + dy*dy) / 2.0), 255)
                data_out[x + w*y] = value
        return out
 
|end_scriptsize|

Version 0, demo
---------------

Demo

|pause|

PyPy is ~23x faster. Cool.


Version 1
---------

|scriptsize|

.. sourcecode:: python

    def get(img, x, y):
        w, h, data = img
        i = x + y*w
        return data[i]

    def set(img, x, y, value):
        w, h, data = img
        i = x + y*w
        data[i] = value

    def sobel(img):
        w, h, data = img
        out = w, h, array.array('B', [0]) * (w*h)
        for y in xrange(1, h-1):
            for x in xrange(1, w-1):
                dx = (-1.0 * get(img, x-1, y-1) +
                       1.0 * get(img, x+1, y-1) +
                      -2.0 * get(img, x-1, y)   +
                       2.0 * get(img, x+1, y)   +
                      -1.0 * get(img, x-1, y+1) +
                       1.0 * get(img, x+1, y+1))
                dy = ...
        ...

|end_scriptsize|


Version 2
---------

|scriptsize|

.. sourcecode:: python

    class Image(object):

        def __init__(self, width, height, data=None):
            self.width = width
            self.height = height
            if data is None:
                self.data = array.array('B', [0]) * (width*height)
            else:
                self.data = data

        def __getitem__(self, idx):
            x, y = idx
            return self.data[x + y*self.width]

        def __setitem__(self, idx, value):
            x, y = idx
            self.data[x + y*self.width] = value

|end_scriptsize|


Version 3
-------------

|scriptsize|

.. sourcecode:: python

    _Point = namedtuple('_Point', ['x', 'y'])
    class Point(_Point):
        def __add__(self, other):
            ox, oy = other
            x = self.x + ox
            y = self.y + oy
            return self.__class__(x, y)

    class ImageIter(object):
        def __init__(self, x0, x1, y0, y1):
            self.it = itertools.product(xrange(x0, x1), xrange(y0, y1))
        def __iter__(self):
            return self
        def next(self):
            x, y = next(self.it)
            return Point(x, y)

    class Image(v2.Image):
        def noborder(self):
            return ImageIter(1, self.width-1, 1, self.height-1)

|end_scriptsize|

Version 3
-------------

|scriptsize|

.. sourcecode:: python

    def sobel(img):
        img = Image(*img)
        out = Image(img.width, img.height)
        for p in img.noborder():
            dx = (-1.0 * img[p + (-1,-1)] +
                   1.0 * img[p + ( 1,-1)] + 
                  -2.0 * img[p + (-1, 0)] +
                   2.0 * img[p + ( 1, 0)] + 
                  -1.0 * img[p + (-1, 1)] +
                   1.0 * img[p + ( 1, 1)])

            dy = (-1.0 * img[p + (-1,-1)] +
                  -2.0 * img[p + ( 0,-1)] +
                  -1.0 * img[p + ( 1,-1)] + 
                   1.0 * img[p + (-1, 1)] +
                   2.0 * img[p + ( 0, 1)] +
                   1.0 * img[p + ( 1, 1)])

            value = min(int(sqrt(dx*dx + dy*dy) / 2.0), 255)
            out[p] = value

|end_scriptsize|
