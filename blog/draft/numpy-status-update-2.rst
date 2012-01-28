Hello.

This is just a quick status update on the NumPy in PyPy project that as of very
recently became my day job. I probably should thank once again to Getco and
Nate Lawson who donated $35000 towards this goal and individual contributors
who donated above $5000.

Recently we (Alex Gaynor, Matti Picus and me) implemented few interesting things
that a lot of people use:

* more ufuncs

* most ufuncs now accept axis parameter (except all and any)

* fixed string representation of arrays, now it's identical to numpy (uses
  pretty much the same code)

* ``ndarray.flat`` should be working correctly

* ``ndarray.flatten``, ``ndarray.ravel``, ``ndarray.take``

* indexing arrays by boolean arrays of the same size

* bugfixes

We would also like to introduce the `nightly report`_ of numpy status. This
is an automated tool that does package introspection. While it gives some
sort of idea how much of numpy is implemented, it's not by far the authority.
Your tests should be the authority. It won't report whether functions
support all kinds of parameters (for example masked arrays and ``out`` parameter
are completely unsupported) or that functions work **at all**.

We hope to provide you with more frequent updates on the progress and in
meantime I would like to encourage people to donate towards the step 2, which
is making it **really** fast.

Cheers,
fijal & the PyPy tem

