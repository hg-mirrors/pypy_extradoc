Py3k status update #12
----------------------

This is the 12th status update about our work on the `py3k branch`_, which we
can work on thanks to all of the people who donated_ to the `py3k proposal`_.

Here's an update on the recent progress:

* Thank you to everyone who has provided initial feedback on the PyPy3 2.1 beta
  1 release. We've gotten a number of bug reports, most of which have been
  fixed.

* As usual, we're continually keeping up with changes from the default
  branch. Oftentimes these merges come at a cost (conflicts and or
  reintegration of py3k changes) but occasionally we get goodies for free, such
  as the `recent JIT optimizations`_ and `incremental garbage collection`_.

* We've been focusing on re-optimizing Python 2 int sized (machine sized)
  integers:

We have a couple of known, notable speed regressions in the PyPy3 beta release
vs regular PyPy. The major one being with Python 2.x int sized (or machine
sized) integers.

Python 3 drops the distinction between int and long types. CPython 3.x
accomplishes this by removing the old int type entirely and renaming the long
type to int. Initially, we've done the same for PyPy3 for the sake of
simplicity and getting everything working.

However PyPy's JIT is capable of heavily optimizing these machine sized integer
operations, so this came with a regression in performance in this area.

We're now in the process of solving this. Part of this work also involves some
house cleaning on these numeric types which also benefits the default branch.

cheers,
Phil

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/commits/all/tip/branch%28%22py3k%22%29

.. _`recent JIT optimizations`: http://morepypy.blogspot.com/2013/10/making-coveragepy-faster-under-pypy.html
.. _`incremental garbage collection`: http://morepypy.blogspot.com/2013/10/incremental-garbage-collector-in-pypy.html
