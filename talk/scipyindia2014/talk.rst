.. include:: beamerdefs.txt

=============================
PyPy and the scientific stack
=============================

Introduction
------------

* PyPy contributor

* Hired to work on NumPyPy

* Interested in library compatibility

* @rguillebert on twitter, feel free to send me questions

* Software consultant

* Feel free to interrupt me

PyPy
----

* PyPy is an implementation of the Python language

* Speed is one of its main advantages

* Compatibility is very important to us

Python
------

* Python is a great language

* Very dynamic

* Easy to introspect (pdb is just another Python module)

* Considered slow

Speed
-----

.. image:: speed.png
   :scale: 50%
   :align: center

How ?
-----

* Tracing Just-In-Time compiler

* Removes overhead

Demo
----

* Real-time edge detection

How to get performance out of Python code ?
-------------------------------------------

* Rewrite your code in C

* Rewrite your code in Cython

* Rewrite your code in some subset/dialect of Python like Numba

* Just write Python and use PyPy, only pay the cost of what you use

PyPy and C (1/2)
----------------

* PyPy is pretty good at interacting with C code now, thanks to CFFI

* CFFI is the easiest tool to I've used so far

* Very fast on PyPy, fast enough on CPython

* Used by NumPyPy

* With CFFI you can call C code from Python and expose Python functions to C 

  - This means you can create your own C API in pure Python !

PyPy and C (2/2)
----------------

* It is now possible to embed PyPy in a C application (uWSGI)

* C extensions written using the Python C API can work, but they're slow and support is incomplete

* We have ideas to help with that in some use cases

Python C API
------------

* Leaks way too many implementation details (refcounting, PyObject structure fields)

* Makes it hard to improve Python while supporting 100% of the API

* Should we have a new C API ?

NumPyPy
-------

* ~80% of the numpy tests are passing

* Most of numpy is there

* XXX is missing

NumPyPy performance
-------------------

* Vectorized operations should be as fast as Numpy

* Using ndarrays as you would use arrays in C or Java should be as fast

* Lazy evaluation ?

PyMetabiosis
------------

* Work in progress

JitPy
-----

* Work in progress

Thank You
---------

Questions ?
