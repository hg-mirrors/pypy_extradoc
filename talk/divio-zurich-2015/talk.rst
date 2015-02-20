====
PyPy
====

Who am I?
---------

* Maciej Fijalkowski

* PyPy core developer

* owner of baroquesoftware.com

What is PyPy?
-------------

* a fast, compliant Python interpreter

* comes with a just in time compiler

* covers Python 2.7 and beta 3.2/3.3

Compatibility status
--------------------

* pure-python code should just run

* C-extensions sometimes work sometimes don't

* library support is large and growing

* numeric is more complicated

Compatibility - C extensions
----------------------------

* CPython C API - compatibility layer (slow, potentially problematic)

* Cython uses that, does not work

* ctypes sort of works, but don't use ctypes

* our solutions is cffi

cffi
----

xxxx image

cffi (2)
--------

* demo

numpy and numerics
------------------

* big subset of numpy reimplemented

* same speed as numpy, much faster with python code

* aim at compatibility

* pymetabiosis (scipy, matplotlib)

Speed status
------------

* speed.pypy.org

Speed status (2)
----------------

* more mudded picture :-)

* a lot of programs are faster (20% to 100x)

* some programs are slower

* warmup time is a key factor

Memory consumption
------------------

* objects are smaller than CPython

* interpreter size is large (~60M)

* additional assembler consumes memory

* plus bookkeeping info

* measure!

Can I run PyPy?
---------------

* mostly, yes!

* look at C extensions

* try, measure, benchmark

Case study - magnetic.com
-------------------------

* magnetic.com - online search retargetting

* 2 weeks of work, including benchmarking and analysis

* swapped ujson for json

* rewrote bindings for protobuf

* ~2x speedup after warmup, no additional noticable memory

Future
------

* work on warmup

* STM work

* more numpy compatibility

Crowdfunding
------------

* moderate success in crowdfunding

* numpy, STM, py3k

* donate

Commercial consulting
---------------------

* baroquesoftware.com

* measure, analyze, port to pypy

Q&A
---

* http://pypy.org

* http://baroquesoftware.com

