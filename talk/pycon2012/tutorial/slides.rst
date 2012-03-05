First rule of optimization?
===========================

|pause|

If it's not correct, it doesn't matter.

Second rule of optimization?
============================

|pause|

If it's not faster, you're wasting time.

|pause|

But if you iterate fast, you can afford wasting time

Third rule of optimization?
===========================

|pause|

Measure twice, cut once.

(C)Python performance tricks
============================

|pause|

* ``map()`` instead of list comprehensions

* ``def f(int=int):``, make globals local

* ``append = my_list.append``, grab bound methods outside loop

* Avoiding function calls

* Don't write Python

Forget these
============

* PyPy has totally different performance characterists

* Which we're going to learn about now

* You cannot speak about operations in isolation (more later)

Why PyPy?
=========

* performance

* memory

* sandbox

Why not PyPy (yet)?
===================

* embedded python interpreter

* embedded systems

* not x86-based systems

* extensions, extensions, extensions

Performance
===========

* the main thing we'll concentrate on today

* PyPy is an interpreter + a JIT

* compiling Python to assembler via magic (we'll talk about it later)

* very different performance characteristics from CPython

Performance sweetspots
======================

* every VM has it's sweetspot

* we try hard to make it wider and wider

CPython's sweetspot
===================

* moving computations to C, example::

   map(operator.attrgetter("a"), my_list)

PyPy's sweetpot
===============

* **simple** python

* if I can't understand it, JIT won't either

How PyPy runs your program, involved parts
==========================================

* a simple bytecode compiler (just like CPython)

* an interpreter loop written in RPython

* a JIT written in RPython

* an assembler backend

Bytecode interpreter
====================

* executing one bytecode at a time

* add opcode for example

* .... goes on and on

* example

Tracing JIT
===========

* once the loop gets hot, it's starting tracing (1039 runs, or 1619 function
  calls)

* generating operations following how the interpreter executes them

* optimizing them

* compiling to assembler (x86, ppc or arm)

PyPy's specific features
========================

* JIT complete by design, as long as the interpreter is correct

* Only **one** language description, in a high level language

* Decent tools for inspecting the generated code

Performance characteristics - runtime
=====================================

* Runtime the same or a bit slower as CPython

* Examples of runtime:

  * ``list.sort``

  * ``long + long``

  * ``set & set``

  * ``unicode.join``

  * ...

Performance characteristics - JIT
=================================

* Important notion - don't consider operations in separation

* Always working as a loop or as a function

* Heuristics to what we believe is common python

* Often much faster than CPython once warm

Heuristics
==========

* What to specialize on (assuming stuff is constant)

* Data structures

* Relative cost of operations

Heuristic example - dicts vs objects
====================================

* Dicts - an unknown set of keys, potentially large

* Objects - a relatively stable, constant set of keys
  (but not enforced)

* Performance example

Specialized lists
=================

* lists are specialized for type - ``int``, ``float``, ``str``, ``unicode`` and
  ``range``.

* appending a new type to an existing list makes you iterate over the entire
  list and rewrite everything.

Itertools abuse
===============

* some examples

* simple is good

* python is vast

* if we've never seen a use of some piece of stdlib, chances are it'll be
  suboptimal on pypy

Obscure stuff
=============

* Frame access is slow

* List comprehension vs generator expression

* Profiling & tracing hooks

* A bit in the state of flux

JitViewer
=========

* http://bitbucket.org/pypy/jitviewer

* ``mkvirtualenv -p <path to pypy>``

* ``python setup.py develop``

The overview
============

* Usually three pieces per loop

* Prologue and two loop iterations (loop invariants in the first bit)

* They contain guards

* Guards can be compiled to more code (bridges) that jump back to the loop
  or somewhere else

* Functions are inlined

* Sometimes completely twisted flow
