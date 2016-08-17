CFFI: calling C from Python
===========================

Abstract (longer version)
-------------------------

I will introduce CFFI, a way to call C libraries from Python.

    http://cffi.readthedocs.org/

CFFI was designed in 2012 to get away from Python's C extension modules,
which require hand-written CPython-specific C code.  CFFI is arguably
simpler to use: you call C from Python directly, instead of going
through an intermediate layer.  It is not tied to CPython's internals,
and works natively on two different Python implementations: CPython and
PyPy.  It could be ported to more implementations.

It is also a big success, according to the download statistics.  Some
high-visibility projects like Cryptography have switched to it.

Part of the motivation for developing CFFI is that it is a minimal layer
that allows direct access to C from Python, with no fixed intermediate C
API.  It shares ideas from Cython, ctypes, and LuaJIT's ffi, but the
non-dependence on any fixed C API is a central point.


It is a possible solution to a problem that hits notably PyPy --- the
CPython C API.  The CPython C API was great and, we can argue, it
contributed a lot to the present-day success of Python, together with
tools built on top of it like Cython and SWIG.  However, it may be time
to look beyond it.  This talk will thus present CFFI as such an example.
This independence is what lets CFFI work equally well on CPython and on
PyPy (and be very fast on the latter thanks to the JIT compiler).


Abstract (short version)
------------------------

In this talk, we will see an intro to CFFI, an alternative to using the
standard C API to extend Python.  CFFI works on CPython and on PyPy.  It
is a possible solution to a problem that hits notably PyPy --- the
CPython C API.

The CPython C API was great and contributed to the present-day success
of Python, together with tools built on top of it like Cython and SWIG.
I will argue that it may be time to look beyond it, and present CFFI as
such an example.
