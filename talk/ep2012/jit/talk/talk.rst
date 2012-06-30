.. include:: beamerdefs.txt

================================
PyPy JIT under the hood
================================

About this talk
----------------

* What is PyPy? (in 30 seconds)

  - (for those who missed the keynote :-))

* Overview of tracing JITs

* The PyPy JIT generator

* JIT-friendly programs


Part 0: What is PyPy?
----------------------

* RPython toolchain

  - subset of Python

  - ideal for writing VMs

  - JIT & GC for free

* Python interpreter

  - written in RPython

* Whatever (dynamic) language you want

  - smalltalk, prolog, javascript, ...


Part 1
------

**Overview of tracing JITs**

Compilers
---------

* When?

  - Batch or Ahead Of Time

  - Just In Time

|pause|

* How?

  - Static

  - Dynamic or Adaptive

|pause|

* What?

  - Method-based compiler

  - Tracing compiler

|pause|

* PyPy: JIT, Dynamic, Tracing
