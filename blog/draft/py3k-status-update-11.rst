Py3k status update #11
----------------------

This is the 11th status update about our work on the `py3k branch`_, which we
can work on thanks to all of the people who donated_ to the `py3k proposal`_.

Here's some highlights of the progress made since the previous update:

* PyPy py3k now matches CPython 3's hash code for
  int/float/complex/Decimal/Fraction

* Various outstanding unicode identifier related issues were
  resolved. E.g. test_importlib/pep263/ucn/unicode all now fully pass. Various
  usage of identifiers (in particular type and module names) have been fixed to
  handle non-ascii names -- mostly around display of reprs and exception
  messages.

* The unicodedata database has been upgraded to 6.0.0.

* Windows support has greatly improved, though it could still use some more
  help (but so does the default branch to a certain degree).

* Probably the last of the parsing related bugs/features have been taken care
  of.

* Of course various other smaller miscellaneous fixes

This leaves the branch w/ only about 5 outstanding failures of the stdlib test
suite:

* test_float

  1 failing test about containment of floats in collections.

* test_memoryview

  Various failures: requires some bytes/str changes among other things (Manuel
  Jacob's has some progress on this on the `py3k-memoryview branch`_)

* test_multiprocessing

  1 or more tests deadlock on some platforms

* test_sys and test_threading

  2 failing tests for the New GIL's new API

Probably the biggest feature left to tackle is the New GIL.

We're now pretty close to pushing an initial release. We had planned for one
around PyCon, but having missed that we've put some more effort into the branch
to provide a more fully-fledged initial release.

Thanks to the following for their contributions: Manuel Jacob, Amaury Forgeot
d'Arc, Karl Ramm, Jason Chu and Christian Hudson.

cheers,
Phil

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/commits/all/tip/branch%28%22py3k%22%29
.. _`py3k-memoryview branch`: https://bitbucket.org/pypy/pypy/compare/py3k-memoryview..py3k
