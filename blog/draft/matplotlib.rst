===================================
Plotting using matplotlib from PyPy
===================================

**Big fat warning** This is just a proof of concept. It barely works. There are
missing pieces left and right, which were replaced with hacks so I can get this
to run and prove it's possible. Don't try this at home, especially your home.
You have been warned.

There has been a lot of talking about PyPy not integrating well with the
current scientific Python ecosystem, and ``numpypy`` (a NumPy reimplementation
on top of pypy) was dubbed "a fancy array library". I'm going to show that
integration with this ecosystem is possible with our design.

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

* The approach is generally portable, however the implementation has not been
  tested on any platforms other than 64-bit Linux. Try anything else at your
  own peril.

* You need to install python2.6, the python2.6 development headers, and have
  numpy and matplotlib installed on that python.

* You need a checkout of my `hacks directory`_ and put embedded on your
  ``PYTHONPATH``, your pypy checkout also has to be on the ``PYTHONPATH``.

Er wait, what happened?
-----------------------

What didn't happen is we did not reimplement matplotlib on top of PyPy. What
did happen is we embed CPython inside of PyPy using ctypes. We instantiate it.
and follow the `embedding`_ tutorial for CPython. Since numpy arrays are not
movable, we're able to pass around an integer that's represents the memory
address of the array data and reconstruct it in the embedded interpreter. Hence
with a relatively little effort we managed to reuse the same array data on both
sides to plot at array. Easy, no?

This approach can be extended to support anything that's not too tied with
python objects. SciPy and matplotlib both fall into the same category
but probably the same strategy can be applied to anything, like GTK or QT.
It's just a matter of extending a hack into a working library.

To summarize, while we're busy making numpypy better and faster, it seems
that all heavy lifting on the C side can be done using an embedded Python
interpreter with relatively little effort. To get to that point, I spent
a day and a half to learn how to embed CPython, with very little prior
experience in the CPython APIs. (XXX: this should make clear that you can use it for integration, but for speed you should keep stuff all in PyPy)

Cheers,
fijal
