CFFI release 0.1
================

Hi.

We're pleased to announce the first public release, 0.1 of CFFI, a way to call C from Python.
(This release does not support PyPy yet --- but we announce it here as it is planned for the
next release :-)

The package is available `on bitbucket`_ as well as `documented`_. You can also install it
straight from the python package index (pip).

The aim of this project is to provide a convenient and reliable way of calling C code from Python.
The interface is based on `LuaJIT's FFI`_ and follows a few principles:

* The goal is to call C code from Python.  You should be able to do so
  without learning a 3rd language: every alternative requires you to learn
  their own language (Cython_, SWIG_) or API (ctypes_).  So we tried to
  assume that you know Python and C and minimize the extra bits of API that
  you need to learn.

* Keep all the Python-related logic in Python so that you don't need to
  write much C code (unlike `CPython native C extensions`_).

* Work either at the level of the ABI (Application Binary Interface)
  or the API (Application Programming Interface).  Usually, C
  libraries have a specified C API but often not an ABI (e.g. they may
  document a "struct" as having at least these fields, but maybe more).
  (ctypes_ works at the ABI level, whereas `native C extensions`_
  work at the API level.)

* We try to be complete.  For now some C99 constructs are not supported,
  but all C89 should be, including macros (and including macro "abuses",
  which you can manually wrap in saner-looking C functions).

* We attempt to support both PyPy and CPython (although PyPy support is not
  complete yet) with a reasonable path for other Python implementations like
  IronPython and Jython.

* Note that this project is **not** about embedding executable C code in
  Python, unlike `Weave`_.  This is about calling existing C libraries
  from Python.

.. _`LuaJIT's FFI`: http://luajit.org/ext_ffi.html
.. _`Cython`: http://www.cython.org
.. _`SWIG`: http://www.swig.org/
.. _`CPython native C extensions`: http://docs.python.org/extending/extending.html
.. _`native C extensions`: http://docs.python.org/extending/extending.html
.. _`ctypes`: http://docs.python.org/library/ctypes.html
.. _`Weave`: http://www.scipy.org/Weave
.. _`on bitbucket`: https://bitbucket.org/cffi/cffi
.. _`documented`: http://cffi.readthedocs.org

Status of the project
---------------------

Consider this as a beta release. Creating CPython extensions is fully supported and the API should
be relatively stable; however, minor adjustements of the API are possible.

PyPy support is not yet done and this is a goal for the next release. There are vague plans to make this the
preferred way to call C from Python that can reliably work between PyPy and CPython.

Right now CFFI's verify() requires a C compiler and header files to be available at run-time.
This limitation will be lifted in the near future and it'll contain a way to cache the resulting binary.

Cheers,
Armin Rigo and Maciej Fijałkowski
