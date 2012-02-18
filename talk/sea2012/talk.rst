Fast numeric in Python - NumPy and PyPy
=======================================

What is this talk about?
------------------------

* what is pypy and why

* numeric landscape in python

* what we achieved in pypy

* where we're going

What is PyPy?
-------------

* **An efficient implementation of Python language**

* A framework for writing efficient dynamic language implementations

* An open source project with a lot of volunteer effort

* I'll talk today about the first part (mostly)

PyPy status right now
---------------------

* An efficient just in time compiler for the Python language

* Relatively "good" on numerics (compared to other dynamic languages)

* Example - real time video processing

* Some comparisons

Why would you care?
-------------------

* "If I write this stuff in C it'll be faster anyway"

* maybe, but ...

Why would you care (2)
----------------------

* Experimentation is important

* Implementing something faster, in human time, leaves more time for optimizations and improvements

* For novel algorithms, being clearly expressed in code makes them easier to evaluate (Python is cleaner than C often)

* Example - memcached server (?) XXX think about it

Numerics in Python
------------------

* ``numpy`` - for array operations

* ``scipy``, ``scikits`` - various algorithms, also exposing C/fortran
  libraries

* ``matplotlib`` - pretty pictures

* ``ipython``

There is an entire ecosystem!
-----------------------------

* Which I don't even know very well

* ``PyCUDA``

* ``pandas``

* ``mayavi``

What's important?
-----------------

* There is an entire ecosystem built by people

* It's available for free, no shady licensing

* It's being expanded

* It's growing

* It'll keep up with hardware advancments

Problems with numerics in python
--------------------------------

* Stuff is reasonably fast, but...

* Only if you don't actually write much Python

* Array operations are fine as long as they're vectorized

* Not everything is expressable that way

* Numpy allocates intermediates for each operation, trashing caches

Our approach
------------

* Build a tree of operations

* Compile assembler specialized for aliasing and operations

* Execute the specialized assembler

Examples
--------

XXX say that the variables are e.g. 1-dim numpy arrays

* ``a + a`` would generate different code than ``a + b``

* ``a + b * c`` is as fast as a loop

Status
------

* This works reasonably well

* Far from implementing the entire numpy, although it's in progress

* Assembler generation backend needs works

* Vectorization in progress

Status benchmarks
-----------------

* laplace solution

* solutions:

  +---+
  |   |
  +---+

This is just the beginning...
-----------------------------

* PyPy is an easy platform to experiment with

