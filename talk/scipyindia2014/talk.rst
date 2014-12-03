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

Speed
-----

* XXX : Insert speed.pypy.org screenshot

Python
------

* Python is a great language

* Very dynamic

* Easy to introspect (pdb is just another Python module)

* Considered slow

How to get performance out of Python code ?
-------------------------------------------

* Rewrite your code in C

* Rewrite your code in Cython

* Rewrite your code in some subset/dialect of Python like Numba

* Just write Python and use PyPy, pay only the cost of what you use

PyPy And C
----------

* PyPy is pretty good at interacting with C code with cffi

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

* XXX
