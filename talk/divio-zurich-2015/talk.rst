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

XXX slide about cffi and demo

Speed status
------------

xxx graph

Speed status (2)
----------------

* more mudded picture :-)

* a lot of programs are faster (20% to 100x)

* some programs are slower

* warmup time is a key factor

Memory consumption
------------------

* objects are smaller than CPython

Can I run PyPy?
---------------

Xxxx

Case study - magnetic
---------------------

