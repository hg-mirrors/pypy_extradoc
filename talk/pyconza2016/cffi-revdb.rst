
CFFI, calling C // RevDB, a new debugger
========================================


Abstract
--------

Two different topics:

* CFFI: a simple way to call C code from your Python programs;

* RevDB: an experimental "reverse debugger" for Python.

The two topics have in common their existence thanks to PyPy, an
alternative Python implementation in Python.  Both are interesting
even if you are only using the regular CPython.

*CFFI* is an alternative to using the standard CPython C API to extend
Python (or other tools like Cython, SWIG or ctypes).  It was
originally inspired by LuaJIT's FFI.  Like Cython, you declare C
functions and compile that with a regular C compiler.  Unlike Cython,
there is no special language: you manipulate C data structures and
call C functions straight from Python.  I will show examples of how
simple it is to call existing C code with CFFI.

*RevDB* is a reverse debugger for Python, similar to UndoDB-GDB or LL
for C.  You run your program once, in "record" mode; then you start
the reverse-debugger on the log file.  It gives a pdb-like experience,
but it is replaying your program exactly as it ran---and moreover you
can now go backward as well as forward in time.  You also get
"watchpoints", which are very useful to find when things change.  I
will show how it works on small examples.
