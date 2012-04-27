STM update (and thanks everybody)
=================================

A short update on the Software Transactional Memory (STM) side.  Let me
remind you that the work is to add STM internally into PyPy, with the
goal of letting the user's programs run on multiple cores after a minor
adaptation.  (The goal is not to expose STM to the user's program.)  I
will soon write some official documentation that explains in more
details exactly what you get.  For now you can read the previous blog__
posts__, and you can also find technical details in the `call for
donation`_ itself; or directly look at how I adapted the examples linked
to later in this post.

.. _`call for donation`: http://pypy.org/tmdonate.html
.. __: http://morepypy.blogspot.com/2012/03/call-for-donations-for-software.html
.. __: http://morepypy.blogspot.com/2012/01/transactional-memory-ii.html

I have now reached the point where the basics seem to work.  There is no
integration with the JIT so far; moreover the integration with the
Garbage Collection subsystem is not finished right now, but at least
"not crashing in my simple tests and not leaking memory too quickly".
(It means that it is never calling ``__del__`` so far, although it
releases memory; and when entering transactional mode or when going to
the next transaction, all live objects become immortal.  This should
still let most not-too-long-running programs work.)

If you want to play with it, you can download `this binary`_ (you need to
put it in a place with the paths ``lib-python`` and ``lib_pypy``, for
example inside the main directory from a regular `nightly tarball`_
or from a full checkout).
This version was compiled for Linux x86 32-bit from the `stm-gc`_ branch
on the 25th of April.  It runs e.g. the modified version of richards_.
This branch could also be translated for Linux x86-64, but not for
other OSes nor other CPUs for now.

.. _`this binary`: http://wyvern.cs.uni-duesseldorf.de/~arigo/pypy-stm-22fccf3c9b5e.tar.bz2
.. _`nightly tarball`: http://buildbot.pypy.org/nightly/trunk/
.. _`stm-gc`: https://bitbucket.org/pypy/pypy/src/stm-gc
.. _richards: https://bitbucket.org/pypy/pypy/raw/stm-gc/pypy/translator/stm/test/richards.py

The resulting ``pypy-stm`` exposes the same interface as the pure Python
transaction_ module, which is an emulator (running on CPython or any
version of PyPy) which can be used to play around and prepare your
programs.  See the comments in there.  A difference is that the real
``pypy-stm`` doesn't support epoll right now, so it cannot be used yet
to play with `a branch of Twisted`_ that was already adapted (thanks
Jean-Paul Calderone); but that's coming soon.  For now you can use it to
get multi-core usage on purely computational programs.

I did for example adapt PyPy's own ``translate.py``: see the tweak `in
rpython/rtyper.py`_.  Lines 273-281 are all that I needed to add, and
they are mostly a "simplification and parallelization" of the lines
above.  There are a few more places in the whole ``translate.py`` that
could be similarly modified, but overall it is just that: a few places.
I did not measure performance, but I checked that it is capable of using
multiple cores in the RTyping step of translation, with --- as expected
--- some still-reasonable number of conflicts, particularly at the
beginning when shared data structures are still being built.

.. _transaction: https://bitbucket.org/pypy/pypy/raw/stm-gc/lib_pypy/transaction.py
.. _`a branch of Twisted`: svn://svn.twistedmatrix.com/svn/Twisted/branches/stm-5526
.. _`in rpython/rtyper.py`: https://bitbucket.org/pypy/pypy/src/stm-gc/pypy/rpython/rtyper.py#cl-249

On a few smaller, more regular examples like richards_, I did measure
the performance.  It is not great, even taking into account that it has
no JIT so far; but it is well within the 2-to-5-times slower goal, and
it does seem to scale.  At least, it scales roughly as expected on my
2-real-cores, 4-hyperthreaded-cores laptop (which means that using two
cores is not quite twice as fast as using only one, and using all four
cores is again not twice faster but only 20-30%).

And finally...

...a big thank you to everyone who contributed some money to support
this!  As you see on the PyPy_ site, we got more than 6700$ so far in
only 5 or 6 weeks.  Thanks to that, my contract started last Monday, and
I am now paid a small salary via the `Software Freedom Conservancy`_
(thanks Bradley M. Kuhn for organizational support from the SFC).
Again, thank you everybody!

.. _PyPy: http://pypy.org/
.. _`Software Freedom Conservancy`: http://sfconservancy.org/
