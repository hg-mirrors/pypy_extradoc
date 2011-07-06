Realtime image processing in Python
===================================

Image processing is notoriusly a CPU intensive task.  To do it in realtime,
you need to implement your algorithm in a fast language, hence trying to do it
in Python is foolish: Python is clearly not fast enough for this task. Is it?
:-)

.. image:: sobel.png

Actually, it turns out that the PyPy JIT compiler produces code which is fast
enough to do realtime video processing using two simple algorithms implemented
by Håkan Ardö.

sobel.py implements a classical way of locating edges in images,
`the Sobel operator`:http://en.wikipedia.org/wiki/Sobel_operator. It
is an approximation of the magnitude of the 
`image gradient`:http://en.wikipedia.org/wiki/Image_gradient. The
processing time is spend on two
`convolutions`:http://en.wikipedia.org/wiki/Convolution between the
image and 3x3-kernels.

magnify.py implements a pixel coordinate transformation that rearranges
the pixels in the image to form a magnifying effect in the center.
It consists of a single loop over the pixels in the output image copying
pixels from the input image. 

You can try by yourself by downloading the appropriate demo:

  - `pypy-image-demo.tar.bz2`_: this archive contains only the source code,
    use this is you have PyPy already installed

  - `pypy-image-demo-full.tar.bz2`_: this archive contains both the source
    code and prebuilt PyPy binaries for linux 32 and 64 bits

.. `pypy-image-demo.tar.bz2`: http://wyvern.cs.uni-duesseldorf.de/~antocuni/pypy-image-demo.tar.bz2
.. `pypy-image-demo-full.tar.bz2`: http://wyvern.cs.uni-duesseldorf.de/~antocuni/pypy-image-demo-full.tar.bz2

To run the demo, you need to have ``mplayer`` installed on your system.  The
demo has been tested only on linux, it might (or not) work also on other
systems::

  $ pypy pypy-image-demo/sobel.py

  $ pypy pypy-image-demo/magnify.py

By default, the two demos uses an example AVI file.  To have more fun, you can
use your webcam by passing the appropriate mplayer parameters to the scripts,
e.g::

  $ pypy demo/sobel.py tv://

By default magnify.py uses
`nearest-neighbor
interpolation.`:http://en.wikipedia.org/wiki/Nearest-neighbor_interpolation
By adding the option -b,
`bilinear interpolation`:http://en.wikipedia.org/wiki/Bilinear_interpolation
will be used instead, which gives smoother result.

  $ pypy demo/magnify.py -b

There is only a single implementation of the algorithm in
magnify.py. The two different interpolation methods are implemented by
subclassing the class used to represent images and embed the
interpolation within the pixel access method. PyPy is able to achieve good
performance with this kind of abstractions because it can inline
the pixel access method and specialize the implementation of the algorithm.
In C++ that kind of pixel access method would be virtual and you'll need to use
templates to get the same effect. XXX: Is that correct?

To have a feeling on how much PyPy is faster than CPython, try to run the demo
with the latter.  On my machine, PyPy runs ``sobel.py`` at ~47.23 fps on
average, while CPython runs it at ~0.08 fps, meaning that PyPy is **590 times
faster**.  On ``magnify.py`` the difference is much less evident, ~26.92 fps
vs ~1.78 fps, and the speedup is "only" 15x.

It must be noted that this is an extreme example of what PyPy can do.  In
particular, you cannot expect (yet :-)) PyPy to be fast enough to run an
arbitrary video processing algorithm in real time, but the demo still proves
that PyPy has the potential to get there.
