.. include:: beamerdefs.txt

================================
PyPy Intro and JIT Frontend
================================

About this talk
----------------

* What is PyPy? What is RPython?

* Tracing JIT 101

* PyPy JIT frontend and optimizer

  - "how we manage to make things fast"


Part 1
-------

**PyPy introduction**

What is PyPy?
--------------

* For most people, the final product:

|scriptsize|

.. sourcecode:: python

    $ pypy
    Python 2.7.10 (173add34cdd2, Mar 15 2016, 23:00:19)
    [PyPy 5.1.0-alpha0 with GCC 4.8.4] on linux2
    >>>> import test.pystone
    >>>> test.pystone.main()
    Pystone(1.1) time for 50000 passes = 0.0473992
    This machine benchmarks at 1.05487e+06 pystones/second

|end_scriptsize|

* More in general: a broader project, ecosystem and community


PyPy as a project
------------------

* ``rpython``: a fancy compiler

  - source code: "statically typed Python with type inference and metaprogramming"

  - fancy features: C-like performance, GC, meta-JIT

  - "like GCC" (it statically produces a binary)

|pause|

* ``pypy``: a Python interpreter

  - "like CPython", but written in RPython

  - CPython : GCC = PyPy : RPython



Important fact
---------------

* We **did not** write a JIT compiler for Python

* The "meta JIT" works with all RPython programs

* The "Python JIT" is automatically generated from the interpreter

* Writing an interpreter is vastly easier than a compiler

* Other interpreters: smalltalk, prolog, ruby, php, ...


The final product
------------------

* ``rpython`` + ``pypy``: the final binary you download and execute

  - a Python interpreter

  - with a GC

  - with a JIT

  - fast



Part 1
------

**Overview of tracing JITs**


Assumptions
-----------

* Pareto Principle (80-20 rule)

  - the 20% of the program accounts for the 80% of the runtime

  - **hot-spots**

* Fast Path principle

  - optimize only what is necessary

  - fall back for uncommon cases

|pause|

* Most of runtime spent in **loops**

* Always the same code paths (likely)


Tracing JIT
-----------

* Interpret the program as usual

* Detect **hot** loops

* Tracing phase

  - **linear** trace

* Compiling

* Execute

  - guards to ensure correctness

* Profit :-)


Tracing JIT phases
-------------------

.. animage:: diagrams/tracing-phases-p*.pdf
   :align: center
   :scale: 100%
