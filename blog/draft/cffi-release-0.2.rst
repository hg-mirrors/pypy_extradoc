CFFI release 0.2
================

Hi everybody,

We released `CFFI 0.2`_ (now as a full release candidate).  CFFI is a
way to call C from Python.

This release is only for CPython 2.6 or 2.7.  PyPy support is coming in
the ``ffi-backend`` branch, but not finished yet.  CPython 3.x would be
easy but requires the help of someone.

The package is available `on bitbucket`_ as well as `documented`_. You
can also install it straight from the python package index (pip).

.. _`on bitbucket`: https://bitbucket.org/cffi/cffi
.. _`CFFI 0.2`: http://cffi.readthedocs.org
.. _`documented`: http://cffi.readthedocs.org

* Contains numerous small changes and support for more C-isms.

* The biggest news is the support for `installing packages`__ that use
  ``ffi.verify()`` on machines without a C compiler.  Arguably, this
  lifts the last serious restriction for people to use CFFI.

* Partial list of smaller changes:
  
  - mappings between 'wchar_t' and Python unicodes
  
  - the introduction of ffi.NULL
  
  - a possibly clearer API for ``ffi.new()``: e.g. ``ffi.new("int *")``
    instead of ``ffi.new("int")``
    
  - and of course a plethora of smaller bug fixes

* CFFI uses ``pkg-config`` to install itself if available.  This helps
  locate ``libffi`` on modern Linuxes.  Mac OS/X support is available too
  (see the detailed `installation instructions`__).  Win32 should work out
  of the box.  Win64 has not been really tested yet.

.. __: http://cffi.readthedocs.org/en/latest/index.html#distributing-modules-using-cffi
.. __: http://cffi.readthedocs.org/en/latest/index.html#macos-10-6


Cheers,
Armin Rigo and Maciej Fijałkowski
