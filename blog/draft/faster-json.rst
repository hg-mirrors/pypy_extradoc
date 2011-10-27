Speeding up JSON encoding in PyPy
=================================

Hi

Recently I spent a bit of effort into speeding up JSON in PyPy. I started with
writing a `benchmark`_, which is admittedly not a very good one, but it's
better than nothing (suggestions on how to improve it are welcome!). XXX:
explain in one line what the benchmark does?

For this particular benchmark, the numbers are as follow. **Note that CPython by
default uses the optimized C extension, while PyPy uses the pure Python one**.
PyPy trunk contains another pure Python version which has been optimized
specifically for the PyPy JIT. Detailed optimizations are described later in
this post.

The number reported is the time taken for the third run, when things are
warmed up. Full session `here`_.

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
ugly and takes significant effort. This approach does not scale well when
there is a lot of code to be written or when there is a very tight coupling
between the part to be rewritten and the rest of the code. Still, people would
expect PyPy to be better at "tasks" and not precisely at running equivalent
code, hence a comparison between the C extension and the pure python version
is sound. Fortunately it's possible to outperform the C extension, but requires
a bit of effort on the programmer side as well.

Often interface between the C and Python part is ugly
-----------------------------------------------------

This is very clear if you look at json module as implemented in CPython's
standard library. Not everything is in C (it would probably be just too
much effort) and the interface to what is in C is guided via profiling not
by what kind of interface makes sense. This especially is evident comparing CPython 2.6 to 2.7.
Just adapting the code to an interface with C made the Python version slower.
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
a few a features that make it much easier to optimize than other ways like
``str.join()`` or ``cStringIO``.

* You can specify the start size, which helps a lot if you can even provide
  a rough estimate on the size of the string (less copying)
* Only append and build are allowed. While  the string is being built you
  can't seek or do anything else. After it's built you can never append any more.
* Unicode version available as well as ``__pypy__.builders.UnicodeBuilder``.

Method calls are ok, immutable globals are ok
---------------------------------------------

PyPy's JIT seems to be good enough for at least the simple cases. Calling
methods for common infrastructure or loading globals (instead of rebinding as
locals) is fast enough and improves code readability.

Copying is expensive
--------------------

If you use regular expressions replace, this would always copy a string as of
now. If you know your regexp is simple, first try to match it if there is
anything to replace in the first place. This is a pretty hard optimization to
do automatically -- simply matching the regular expression can be too costly
for it to make sense. In our particular example however, the regexp is really
simple, checking ranges of characters. It also seems that this is by far the
fastest way to escape characters as of now.

Generators are slower than they should be
-----------------------------------------

I changed the entire thing to simply call ``builder.append`` instead of
yielding to the main loop where it would be gathered. This is kind of a PyPy
bug that using generators extensively is slower, but a bit hard to fix.
Especially in cases where there is relatively little data being passed around
(few bytes), it makes sense to gather it first. If I were to implement an
efficient version of ``iterencode``, I would probably handle chunks of
predetermined size, about 1000 bytes instead of yielding data every few bytes.

I must admit I worked around PyPy's performance bug
---------------------------------------------------

For obscure (although eventually fixable) reasons, this::

  for c in s: # s is string
    del c

is faster than::

  for c in s:
    pass

This is a PyPy performance bug and should be fixed, but on a different branch ;-)

PyPy's JIT is good
--------------------------

I was pretty surprised, but the JIT actually did make stuff work nicely.
The changes that were done were relatively minor and straightforward, once
the module was cleaned to the normal "pythonic" state.
It is worth noting that it's possible to write code in Python and make it
run really fast, but you have to be a bit careful. Again, jitviewer is your
friend when determining why things are slow. I hope we can write more tools
in the future that would more automatically guide people through potential
performance pitfals.

Cheers,
fijal
