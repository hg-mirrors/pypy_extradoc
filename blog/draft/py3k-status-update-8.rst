Py3k status update #8
---------------------

This is the eight status update about our work on the `py3k branch`_, which
we can work on thanks to all of the people who donated_ to the `py3k
proposal`_.

Just a short update on November's work: we're now passing about 194 of
approximately 355 modules of CPython's regression test suite, up from passing
160 last month. Many test modules only fail a small number of individual tests
now.

We'd like to thank Amaury Forgeot d'Arc for his contributions, in particular he
has made significant progress on updating `CPyExt`_ for Python 3 this month.

Some other highlights:

* test_marshal now passes, and there's been significant progress on pickling
  (thanks Kenny Levinsen and Amaury for implementing int.to/from_bytes)

* We now have a _posixsubprocess module

* More encoding related fixes, which affects many failing tests

* _sre was updated and now test_re almost passes

* Exception behavior is almost complete per the Python 3 specs, what's mostly
  missing now are the new __context__ and __traceback__ attributes (`PEP
  3134`_)

* Fixed some crashes and deadlocks occurring during the regression tests

cheers,
Philip&Antonio

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/src/py3k
.. _`CPyExt`: http://morepypy.blogspot.com/2010/04/using-cpython-extension-modules-with.html
.. _`PEP 3134`: http://www.python.org/dev/peps/pep-3134/
