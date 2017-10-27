Hello.

This is just a quick status update on the NumPy in PyPy project that very
recently became my day job. I should give my thanks once again to Getco,
Nate Lawson and other contributors who donated above $40000 towards the goal.

Recently we (Alex Gaynor, Matti Picus and me) implemented a few interesting things
that a lot of people use:

* more ufuncs

* most ufuncs now accept the ``axis`` parameter (except ``all`` and ``any``)

* fixed string representation of arrays, now it's identical to numpy (uses
  pretty much the same code)

* ``ndarray.flat`` should be working correctly

* ``ndarray.flatten``, ``ndarray.ravel``, ``ndarray.take``

* indexing arrays by boolean arrays of the same size

* and various bugfixes.

We would also like to introduce the `nightly report`_ of numpy status. This
is an automated tool that does package introspection. While it gives some
sort of idea how much of numpy is implemented, it's not by far the authority.
Your tests should be the authority. It won't report whether functions
support all kinds of parameters (for example masked arrays and ``out`` parameter
are completely unsupported) or that functions work **at all**. We also
reserve the right to incorporate jokes in that website, so don't treat it
that seriously overall :-)

Thanks, and stay tuned.  We hope to post here regular updates on the
progress.

Cheers,
fijal & the PyPy team

.. _`nightly report`: http://buildbot.pypy.org/numpy-status/latest.html
