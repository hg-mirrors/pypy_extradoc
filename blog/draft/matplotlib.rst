===================================
Plotting using matplotlib from PyPy
===================================

**Big fat warning** This is just a proof of concept. It actually barely works.
There are missing pieces left and right there were replaced with hacks so
I can get this to run and show it's possible. Don't try that at home,
especially your home. You have been warned.

There was a lot of talking about PyPy not integrating well with the current
scientific python ecosystem and numpypy (a numpy reimplementation on top
of pypy) was dubbed "a fancy array library". I'm going to show it is possible.

First, `the demo`_::

  #!/usr/bin/env pypy

  # numpy, pypy version
  import numpypy as numpy
  # DRAGONS LIVE THERE (fortunately hidden)
  from embed.emb import import_mod

  pylab = import_mod('matplotlib.pylab')

  if __name__ == '__main__':
      a = numpy.arange(100, dtype=int)
      b = numpy.sin(a)
      pylab.plot(a, b)
      pylab.show()

And you get:

   XXX pic

Now, how to reproduce it:

* You need a PyPy without cpyext, I did not find a linker that would support
  overriding symbols. Right now there are no nightlies like this, so you have
  to compile it yourself, like::

    ./translate.py -Ojit targetpypystandalone.py --withoutmod-cpyext

  That would give you a PyPy that's unable to load some libraries like PIL, but
  perfectly working otherwise.

* Speaking of which, you need a reasonably recent PyPy.

* The approach is generally portable, however the implementation is not. Works
  on 64bit linux, would not bet for anything else.

* You need to install python2.6, python2.6 development headers and have numpy
  and matplotlib installed on that python.

* You need a checkout of my `hacks directory`_ and put embedded on your
  ``PYTHONPATH``, pypy checkout also has to be on the ``PYTHONPATH``.

Er wait, what happened?
-----------------------

What didn't happen is we did not reimplement matplotlib on top of PyPy. What
did happen is we run a CPython instance in PyPy using ctypes. We instantiate
it and nicely follow `embedding`_ tutorial for CPython. Since numpy arrays
are not movable, we're able to pass around an integer that's a pointer to array
data and reconstruct it in the embedded interpreter. Hence with a relatively
little effort we managed to reuse the sama array data on both sides to
plot at array. Easy, no?

This approach can be extended to support anything that's not too tied with
python objects. SciPy and matplotlib both fall into the same category
but probably the same strategy can be applied to anything, like GTK or QT.
It's just a matter of extending a hack into a working library.

To summarize, while we're busy making numpypy better and faster, it seems
that all heavy lifting on the C side can be done using an embedded Python
interpreter with relatively little effort. To get to that point, I spent
a day and a half to learn how to embed CPython, with very little prior
experience in the CPython APIs.

Cheers,
fijal
