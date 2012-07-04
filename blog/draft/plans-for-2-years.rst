What we'll be busy for the forseeable future
============================================

Hello.

The PyPy dev process has been dubbed as too opaque. In this blog post
we try to highlight a few projects being worked on or in plans for the near
future. As it usually goes with such lists, don't expect any deadlines,
it's more "a lot of work that will keep us busy". It also answers
whether or not PyPy has achieved its total possible performance.

Here is the list of areas, mostly with open branches. Note that the list is
not exhaustive - in fact it does not contain all the areas that are covered
by funding, notably numpy, STM and py3k.

Iterating in RPython
====================

Right now code that has a loop in RPython can be surprised by receiving
an iterable it does not expect. This ends up with doing an unnecessary copy
(or two or three in corner cases), essentially forcing an iterator.
An example of such code would be::

  import itertools
  ''.join(itertools.repeat('ss', 10000000))

Would take 4s on PyPy and .4s on CPython. That's absolutely unacceptable :-)

More optimized frames and generators
====================================

Right now generator expressions and generators have to have full frames,
instead of optimized ones like in the case of python functions. This leads
to inefficiences. There is a plan to improve the situation on the
``continuelet-jit-2`` branch. ``-2`` in branch names means it's hard and
has been already tried unsuccessfully :-)

A bit by chance it would make stackless work with the JIT. Historically though,
the idea was to make stackless work with the JIT and later figured out this
could also be used for generators. Who would have thought :)

This work should allow to improve the situation of uninlined functions
as well.

Dynamic specialized tuples and instances
========================================

PyPy already uses maps. Read our `blog`_ `posts`_ about details. However,
it's possible to go even further, by storing unboxed integers/floats
directly into the instance storage instead of having pointers to python
objects. This should improve memory efficiency and speed for the cases
where your instances have integer or float fields.

Tracing speed
=============

PyPy is probably one of the slowest compilers when it comes to warmup times.
There is no open branch, but we're definitely thinking about the problem :-)

Bridge optimizations
====================

Another "area of interest" is bridge generation. Right now generating a bridge
from compiled loop "forgets" some kind of optimization information from the
loop.

GC pinning and I/O performance
==============================

``minimark-gc-pinning`` branch tries to improve the performance of the IO.

32bit on 64bit
==============
