.. include:: beamerdefs.txt

============================================================
PyPy
============================================================


PyPy is...
--------------------------

* Another Python interpreter

* with a JIT compiler


PyPy was...
-------------------

* Around since 2003

* (advertised as) production ready since December 2010

  - release 1.4

* Funding

  - EU FP6 programme

  - Eurostars programme

  - donations

  - ...


PyPy 1.9: current status
------------------------

* Faster

  - **1.7x** than 1.5 (Summer 2011)

  - **2.2x** than 1.4 (December 2010)

  - **5.5x** than CPython

* Implements Python 2.7.3

* Many more "PyPy-friendly" programs than before

* Packaging

  - |scriptsize| Debian, Ubuntu, Fedora, Homebrew, Gentoo, ArchLinux, ... |end_scriptsize|

  - |scriptsize| Windows (32bit only), OS X |end_scriptsize|

* C extension compatibility

  - runs (big part of) **PyOpenSSL** and **lxml**


PyPy organization
-----------------

* Part of SFC -- Software Freedom Conservancy

  - Bradley successfully fighting U.S. bureaucracy

  - we are happy about it


* Funding model

  - py3k, numpy, STM

  - more than 100'000$ in donations

  - from individuals, large companies and the PSF


PyPy's JIT compiler
-------------------

* Removes abstraction

* Almost never gives up

* x86-32, x86-64, ARMv7, (POWER64)

* (Works with other languages)


Real world applications
-----------------------

* Positive feedback

* http://speed.pypy.org/

* demo


py3k
------------------------

* ``py3k`` branch in mercurial

  - developed in parallel

  - Python 3 written in Python 2

* Focus on correctness

* Dropped some interpreter optimizations for now

* First 90% done, remaining 90% not done

* Majority of the funds by Google


NumPy
-----

* progress going slowly

* multi dimensional arrays, broadcasting, fancy indexing

* all dtypes, except complex, strings and objects

* good results for performance


STM
---------------------------

* Software Transactional Memory

* "Remove the GIL"

* But also, new models (better than threads)

* demo


Calling C
---------

.. image:: standards.png
   :scale: 60%
   :align: center

Calling C landscape
-------------------

* CPython C extensions

* SWIG, SIP, wrapper generators

* ctypes

* Cython

* CFFI (our new thing)

CFFI
----------

|scriptsize|
|example<| Example |>|

  .. sourcecode:: pycon

   >>> from cffi import FFI
   >>> ffi = FFI()
   >>> ffi.cdef("""
   ...     int printf(const char *format, ...);
   ... """)
   >>> C = ffi.dlopen(None)
   >>> arg = ffi.new("char[]", "world")
   >>> C.printf("hi there, %s!\n", arg)
   hi there, world!

|end_example|
|end_scriptsize|

CFFI
----

* Many more examples

* Including macro calls and most subtleties of C

* http://cffi.readthedocs.org


Conclusion
----------

* Try out PyPy on real code

* http://pypy.org/

* Thank you!
