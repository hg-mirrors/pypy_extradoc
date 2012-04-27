STM update (and thanks everybody)
=================================

A short update on the Software Transactional Memory (STM) side.  I have
now reached the point where the basics seem to work, and the integration
with the Garbage Collection subsystem is --- not done by far, but at
least "not crashing in my simple tests and not leaking memory too
quickly".  (It is leaking a bit of memory though, and it is never
calling ``__del__`` so far.)

If you want to play with it, you can download `this binary`_ (you need to
put it in a place with the paths ``lib-python`` and ``lib_pypy``, for
example from a regular `nightly tarball`_ or from a full checkout).  It
is for Linux x86 32-bit.
This version was compiled from the `stm-gc`_ branch on the 25th of April.
It runs e.g. the `modified version of richards`_.
This branch could also be translated for Linux x86-64,
but I didn't do fixes for other platforms for now.

.. _`this binary`: http://wyvern.cs.uni-duesseldorf.de/~arigo/pypy-stm-22fccf3c9b5e.tar.bz2
.. _`nightly tarball`: http://buildbot.pypy.org/nightly/trunk/
.. _`stm-gc`: https://bitbucket.org/pypy/pypy/src/stm-gc
.. _`modified version of richards`: https://bitbucket.org/pypy/pypy/raw/stm-gc/pypy/translator/stm/test/richards.py

It exposes the same interface as the pure Python transaction_ module
(except of course that it's not using the naive implementation linked
above, but its own).  A difference is that it
doesn't support epoll right now, so it cannot be used to play with `a
branch of Twisted`_; but that's coming soon.  For now you can use it to
get multi-core usage on purely computational programs, like PyPy's own
``translate.py`` --- for that I did a tweak `in rpython/rtyper.py`_ (lines
273-281 are all that I needed to add), but there are a few more places
in the whole ``translate.py`` that could be similarly enhanced.

.. _transaction: https://bitbucket.org/pypy/pypy/raw/stm-gc/lib_pypy/transaction.py
.. _`a branch of Twisted`: svn://svn.twistedmatrix.com/svn/Twisted/branches/stm-5526
.. _`in rpython/rtyper.py`: https://bitbucket.org/pypy/pypy/src/stm-gc/pypy/rpython/rtyper.py#cl-249

The performance is not great, even taking into account that it has no
JIT so far, but it seems to scale; at least, it does scale on my
2-real-cores, 4-hyperthreaded-cores laptop, roughly as expected.

And...

...a big thank you to everyone who contributed some money to support
this!  As you see on the PyPy_ site, we got more than 6700$ so far in
only 5 or 6 weeks.  Thanks to that, my contract started last Monday, and
I am now paid a small salary via the `Software Freedom Conservancy`_
(thanks Bradley M. Kuhn for organizational support from the SFC).
Again, thank you everybody!

.. _PyPy: http://pypy.org/
.. _`Software Freedom Conservancy`: http://sfconservancy.org/
