Speeding up JSON encoding in PyPy
=================================

Hi

Recently I spent a bit of effort into speeding up JSON in PyPy. I started with
writing a `benchmark`_, which is admiteddly not very good, but it's better
than nothing (suggestions to improve welcomed!).

For this particular benchmark, the numbers are as follow. Note that CPython
uses hand-optimized C extension and PyPy uses a pure python version,
hand-optimized in trunk, default in older versions. I'm taking the third run,
when things are warmed up, full session `here`_.

+----------------------------+-------------+
| CPython 2.6                | 22s         |
+----------------------------+-------------+
| CPython 2.7                | **3.7s**    |
+----------------------------+-------------+
| CPython 2.7 no C extension | 44s         |
+----------------------------+-------------+
| PyPy 1.5                   | 34s         |
+----------------------------+-------------+
| PyPy 1.6                   | 22s         |
+----------------------------+-------------+
| PyPy trunk                 | **3.3s**    |
+----------------------------+-------------+

.. _`benchmark`: https://bitbucket.org/pypy/benchmarks/src/f04d6d63ba60/own/json_bench.py
.. _`here`: http://paste.pocoo.org/show/498988/

Lessons learned:

Expectations are high
---------------------

A lot of performance critical stuff in Python world is already written in a hand
optimized C. Writing C (especially when you interface with CPython C API) is
ugly and takes significant effort so it's only true for places which are
well separated enough, but still. People would expect PyPy to outperform
C extensions. Fortunately it's possible, but requires a bit of effort on
the programmer side as well.

Often interface between the C and Python part is ugly
-----------------------------------------------------

This is very clear if you look at json module as implemented in CPython's
standard library. Not everything is in C (it would probably be just too
much effort) and the interface to what is in C is guided via profiling not
via what kind of interface makes sense. It's clear from CPython 2.6 to 2.7.
Just adapting the code to interface with C made the Python version slower.
Removing this clutter improves the readability a lot and improves PyPy's version
a bit, although I don't have hard numbers.

JitViewer is crucial
--------------------

In case you're fighting with PyPy's performance, `jitviewer`_ is worth a shot.
While it's not completely trivial to understand what's going on, it'll
definitely show you what kind of loops got compiled and how.

.. _`jitviewer`: https://bitbucket.org/pypy/jitviewer

No nice and fast way to build strings in Python
-----------------------------------------------

PyPy has a custom thing called ``__pypy__.builders.StringBuilder``. It has
few features that make it much easier to optimize than other ways like
``str.join()`` or ``cStringIO``.

* You can specify the start size. Helps a lot if you can even provide a rough
  estimate on the size of the string (less copying)
* Only append and build allowed. While string is built you can't seek or
  do anything else. Once it's built you can never append any more.
* Unicode version available as well as ``__pypy__.builders.UnicodeBuilder``.

Method calls are ok, immutable globals are ok
---------------------------------------------

PyPy's JIT seem to be good enough than at least in simple cases, calling
methods for common infrastructure or loading globals (instead of rebinding as
locals) is fast enough and improves code readability.

I must admit I worked around PyPy's performance bug
---------------------------------------------------

For reasons obscure (although fixable), this::

  for c in s: # s is string
    del c

is faster than::

  for c in s:
    pass

This is a bug and should be fixed, but on different branch ;-)

PyPy's JIT is kind of good
--------------------------

I was pretty surprised, but the JIT actually did make stuff work nicely. Seems
you can write code in Python if you want to make it run fast, but you have
to be a bit careful. Again, jitviewer is your friend

Cheers,
fijal
