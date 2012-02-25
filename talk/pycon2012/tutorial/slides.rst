First rule of optimization?
===========================

|pause|

If it's not correct, it doesn't matter.

Second rule of optimization?
============================

|pause|

If it's not faster, you're wasting ime.

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

Forget these
============

* PyPy has totally different performance characterists

* Which we're going to learn about now

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

* if you can't understand it, JIT won't either

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

* XXX example 1

Tracing JIT
===========

* once the loop gets hot, it's starting tracing (1039 runs, or 1619 function
  calls)

* generating operations following how the interpreter would execute them

* optimizing them

* compiling to assembler (x86 only for now)

PyPy's specific features
========================

* JIT complete by design, as long as the interpreter is correct

* Only **one** language description, in a high level language

* Decent tools for inspecting the generated code

XXXXXXXXXXXXXXXXXXXXXXXXXXXX


* Sweetspot?

  * CPython's sweetspot: stuff written in C

  * PyPy's sweetspot: lots of stuff written in Python

* http://speed.pypy.org

* How do you hit the sweetspot?

  * Be in this room for the next 3 hours.

Memory
======

* PyPy memory usage is difficult to estimate.
* Very program dependent.
* Learn to predict!

Sandbox
=======

* We're not going to talk about it here.
* Run untrusted code.
