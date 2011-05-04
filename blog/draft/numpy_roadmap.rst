
Numpy in PyPy - status and roadmap
==================================

Hello.

NumPy integration is one of the single most requested features for PyPy. This
post tries to describe where we are, what we plan (or what we don't plan), and
how you can help.

**Short version for the impatient: we are doing experiments, which show that
PyPy+numpy can be faster and better than CPython+numpy.  We have a plan on how
to do it, but at the moment there is lack of dedicated people or money to tackle
that.**

The longer version
------------------

Integrating numpy in PyPy has been my pet project on an on-and-off (mostly
off) basis over the past two years. There were `some experiments`_, then
a long pause, and then some more experiments which are documented below.

The general idea is **not** to use the existing CPython module, but to
reimplement numpy in RPython (i.e., the language PyPy is implemented in), thus
letting our JIT achieve extra speedups. The really cool thing about this part
is that numpy will automatically benefit of any general JIT improvements,
without any need of extra tweaking.

At the moment, there is branch called `numpy-exp`_ which contains a
translatable version of a very minimal version of numpy in the module called
``micronumpy``. `Example benchmarks`_ show the following:

XXX: you should briefly describe what the benchmarks do

+--------------------------------+---------------+-------------+
|                                | add           | iterate     |
+--------------------------------+---------------+-------------+
| CPython 2.6.5 with numpy 1.3.0 | 0.260s (1x)   | 4.2 (1x)    |
+--------------------------------+---------------+-------------+
| PyPy numpy-exp @ 3a9d77b789e1  | 0.120s (2.2x) | 0.087 (48x) |
+--------------------------------+---------------+-------------+

The ``add`` benchmark spends most of the time inside the ``+`` operator
between arrays, which in CPython is implemented in C.  As you can see from the
table above, the PyPy version is ~2 times faster. (Although numexpr_ is still
faster than PyPy, but we're working on it).

The exact way how array addition is implemented is worth another blog post, but
in short it lazily evaluates the expression forcing it at the end and avoiding
intermediate results. This way scales much better than numexpr and can lead to
speeding up all the operations that you can perform on matrices.

``iterate`` is even more interesting, because it spends most of the time
inside a Python loop: the PyPy version is ~48 times faster, because the JIT
can optimize across the python/numpy boundary, showing the potential of this
approach.

The next obvious step to get even more speedups would be to extend the JIT to
use SSE operations on x86 CPUs, which should speed it up by about additional
2x.

The drawback of this approach is that we need to reimplement numpy in RPython,
which takes time.  A very rough estimate is that it would be possible to
implement an useful subset of it (for some definition of useful) in a period
of time comprised between one and three man-months.

It also seems that the result will be faster for most cases and the same speed
as original numpy for other cases. The only problem is finding the dedicated
persons willing to spend quite some time on this and however, I am willing to
both mentor such a person and encourage him or her.

Another option would be to sponsor NumPy development. In case you're
interested, please get in touch with us or leave your email in comments.

Cheers,
fijal

.. _`some experiments`: http://morepypy.blogspot.com/2009/07/pypy-numeric-experiments.html
.. _`numpy-exp`: https://bitbucket.org/pypy/pypy/src/numpy-exp/
.. _`Example benchmarks`: https://bitbucket.org/pypy/pypy/src/numpy-exp/pypy/module/micronumpy/bench
