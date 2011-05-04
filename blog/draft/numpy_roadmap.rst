
Numpy in PyPy - status and roadmap
==================================

Hello

Among things people really want to have in PyPy is numpy integration.
This post tries to describe where we are, what we plan (or what we don't plan)
and how you can help.

**The short version for impatient: there are experiments being done, which are
already faster and better than numpy, and there
is a path forward, but there is a definite lack of dedicated people or money
to tackle that.**

The longer version
------------------

The numpy effort in PyPy was my project for a while on an on-and-off (mostly
off) basis over the past two years. There were `some experiments`_ then
mostly nothing and then some more experiments that are documented below.

The general idea that seems to be worthwhile pursuing would be to implement
numpy in RPython (an implementation language of PyPy) and then leverage
JIT to achieve extra speedups. The really cool thing about this part is that
overall JIT improvements will benefit numpy performance out of the box, without
the extra tweaking. As of now there is branch called `numpy-exp`_ which contains
a translatable version of a very minimal version of numpy in the module
called micronumpy. `Example benchmarks`_ show the following:

+--------------------------------+---------------+-------------+
|                                | add           | iterate     |
+--------------------------------+---------------+-------------+
| CPython 2.6.5 with numpy 1.3.0 | 0.260s (1x)   | 4.2 (1x)    |
+--------------------------------+---------------+-------------+
| PyPy numpy-exp @ 3a9d77b789e1  | 0.120s (2.2x) | 0.087 (48x) |
+--------------------------------+---------------+-------------+

As you can see, the moment floats cross the numpy-python boundary, PyPy's
JIT goes blazingly fast, but even running array addition is faster by
a fair degree (although numexpr is still faster, we're working on it).

The exact way how array addition is implemented is worth another blog post,
but in short it lazily evaluates the expression forcing it at the end
and avoiding intermediate results. This way scales much better than numexpr
and can lead to speeding up all the operations that you can perform on matrices.

The next obvious step would be to extend the JIT to use SSE operations on
intel x86 architecture which should speed it up by about additional 2x.

Overall it seems pretty obvious that reimplementing numpy in PyPy (in RPython)
can bring most of the useful compatibility within a month-two-three of work.
It also seems that the result will be faster for most cases and the same speed
as original numpy for other cases. The only problem is finding the dedicated
person willing to spend quite some time on that and personally I would be
willing to both mentor such a person and encourage him or her :)

Another option would be to sponsor numpy development. In case you're interested,
please get in touch with us or leave your email in comments.

Cheers,
fijal

.. _`some experiments`: http://morepypy.blogspot.com/2009/07/pypy-numeric-experiments.html
.. _`numpy-exp`: https://bitbucket.org/pypy/pypy/src/numpy-exp/
.. _`Example benchmarks`: https://bitbucket.org/pypy/pypy/src/numpy-exp/pypy/module/micronumpy/bench
