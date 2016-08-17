
Software Transactional Memory lisp experiments
==============================================

As covered in `the previous blog post`_, the STM subproject of PyPy has been
back on the drawing board. The result of this experiment is an STM-aware
garbage collector written in C. This is finished by now, thanks to Armin's
and Remi's work, we have a fully functional garbage collector and a STM system
that can be used from any C program with enough effort. Using it is more than
a little mundane, since you have to inserts write and read barriers by hand
everywhere in your code that reads or writes to garbage collector controlled
memory. In the PyPy integration, this manual work is done automatically
by the STM transformation in the interpreter.

However, to experiment some more, we created a minimal
`lisp-like/scheme-like interpreter`_
(called Duhton), that follows closely CPython's implementation strategy.
For anyone familiar with CPython's source code, it should be pretty
readable. This interpreter works like a normal and very basic lisp variant,
however it comes with a ``transaction`` builtin, that lets you spawn transactions
using the STM system. We implemented a few demos that let you play with the
transaction system. All the demos are running without conflicts, which means
there are no conflicting writes to global memory and hence the demos are very
amenable to parallelization. They exercise:

* arithmetics - ``demo/many_sqare_roots.duh``

* read-only access to globals - ``demo/trees.duh``

* read-write access to local objects - ``demo/trees2.duh``

With the latter ones being very similar to the classic gcbench. STM-aware
Duhton can be found in `the stmgc repo`_, while the STM-less Duhton,
that uses refcounting, can be found in `the duhton repo`_ under the ``base``
branch.

Below are some benchmarks. Note that this is a little comparing apples to
oranges since the single-threaded duhton uses refcounting GC vs generational
GC for STM version. Future pypy benchmarks will compare more apples to apples.
Moreover none of the benchmarks has any conflicts. Time is the total time
that the benchmark took (not the CPU time) and there was very little variation
in the consecutive runs (definitely below 5%).

+-----------+---------------------+----------------+-----------+-----------+
| benchmark | 1 thread (refcount) | 1 thread (stm) | 2 threads | 4 threads |
+-----------+---------------------+----------------+-----------+-----------+
| square    | 1.9s                | 3.5s           | 1.8s      | 0.9s      |
+-----------+---------------------+----------------+-----------+-----------+
| trees     | 0.6s                | 1.0s           | 0.54s     | 0.28s     |
+-----------+---------------------+----------------+-----------+-----------+
| trees2    | 1.4s                | 2.2s           | 1.1s      | 0.57s     |
+-----------+---------------------+----------------+-----------+-----------+

As you can see, the slowdown for STM vs single thread is significant
(1.8x, 1.7x, 1.6x respectively), but still lower than 2x. However the speedup
from running on multiple threads parallelizes the problem almost perfectly.

While a significant milestone, we hope the next blog post will cover
STM-enabled pypy that's fully working with JIT work ongoing.

Cheers,
fijal on behalf of Remi Meier and Armin Rigo

.. _`the previous blog post`: http://morepypy.blogspot.com/2013/06/stm-on-drawing-board.html
.. _`lisp-like/scheme-like interpreter`: https://bitbucket.org/arigo/duhton
.. _`the stmgc repo`: https://bitbucket.org/pypy/stmgc
.. _`the duhton repo`: https://bitbucket.org/arigo/duhton

