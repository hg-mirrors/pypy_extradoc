
Software Transactional Memory lisp experiments
==============================================

As covered in `the previous blog post`_, the STM subproject of PyPy has been
back on the drawing board. The result of this experiment is an STM-aware
garbage collector written in C. This is finished by now, thanks to Armin's
and Remi's work, we have a fully functional garbage collector and a STM system
that can be used from any C program with enough effort. Using it is more than
a little mundane, since you have to inserts write and read barriers by hand
everywhere in your code that reads or writes to garbage collector controlled
memory. Once we finish PyPy integration, this manual work is done automatically
by the STM transformation in the interpreter.

However, to experiment some more, we created a `lisp interpreter`_
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
