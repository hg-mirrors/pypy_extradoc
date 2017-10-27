CFFI release 0.3
================

Hi everybody,

We released `CFFI 0.3`_.  This is the first release that supports more
than CPython 2.x ``:-)``

* CPython 2.6, 2.7, and **3.x** are supported.

* **PyPy trunk** is supported.

.. _`CFFI 0.3`: http://cffi.readthedocs.org

In more details, the main news are:

* support for PyPy.  You need to get a trunk version of PyPy, which
  comes with the built-in module ``_cffi_backend`` to use with the CFFI
  release.  For testing, you can download the `Linux 32/64 versions of
  PyPy trunk`__.  The OS/X and Windows versions of ``_cffi_backend``
  are not tested at all so far, so probably don't work yet.

* support for Python 3.  It is unknown which exact version is
  required; probably 3.2 or even earlier, but we need 3.3 to run the
  tests.  It runs out of the same sources.

* the main change in the API is that you need to use ``ffi.string(cdata)``
  instead of ``str(cdata)`` or ``unicode(cdata)``.  The motivation for this
  change was the Python 3 compatibility.  If your Python 2 code used to
  contain ``str(<cdata 'char *'>)``, it would interpret the memory content
  as a null-terminated string; but on Python 3 it would just return a
  different string, namely ``"<cdata 'char *'>"``, and proceed without even
  a crash, which is bad.  So ffi.string() solves it by always returning
  the memory content as an 8-bit string (which is a str in Python 2 and
  a bytes in Python 3).

* other minor API changes are documented at
  http://cffi.readthedocs.org/ (grep for ``version 0.3``).

.. __: http://buildbot.pypy.org/nightly/trunk/

Upcoming work, to be done before release 1.0:

* expose to the user the module ``cffi.model`` in a possibly refactored
  way, for people that don't like (or for some reason can't easily use)
  strings containing snippets of C declarations.  We are thinking about
  refactoring it in such a way that it has a ctypes-compatible
  interface, to ease porting existing code from ctypes to cffi.  Note
  that this would concern only the C type and function declarations, not
  all the rest of ctypes.

* CFFI 1.0 will also have a corresponding PyPy release.  We are thinking
  about calling it PyPy 2.0 and including the whole of CFFI (instead of
  just the ``_cffi_backend`` module like now).  In other words it will
  support CFFI out of the box --- we want to push forward usage of CFFI
  in PyPy ``:-)``


Cheers,

Armin Rigo and Maciej Fijałkowski
