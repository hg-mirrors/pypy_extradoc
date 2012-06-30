.. include:: beamerdefs.txt

============================================
PyPy: current status and the GIL-less future
============================================

PyPy at EuroPython
------------------

::

  fijal@helmut:~/src/extradoc/talk$ cd ep20
  ep2004-pypy/ ep2006/      ep2008/      ep2010/      ep2012/      
  ep2005/      ep2007/      ep2009/      ep2011/ 

|pause|

* for those who missed previous EPs, PyPy is a Python interpreter
  with a JIT.

Software archeology
-------------------

"""A foreword of warning about the JIT of PyPy as of March 2007: single
functions doing integer arithmetic get great speed-ups; about anything
else will be a bit slower with the JIT than without.  We are working
on this - you can even expect quick progress, because it is mostly a
matter of adding a few careful hints in the source code of the Python
interpreter of PyPy."""

Software archeology
-------------------

* Around since 2003

* (adverstised as) production ready since December 2010

  - release 1.4

* Funding

  - EU FP6 programme

  - EU FP7 programme

  - donations

  - ...

Current status
--------------

* PyPy 1.9

  - **1.7x** faster than 1.5 (a year ago)

  - **2.2x** faster than 1.4

  - **5.5x** faster than CPython

* much more "PyPy-friendly" programs

* Implements Python 2.7.2

* packaging: Debian, Ubuntu, Fedora, Homebrew, Gentoo, ArchLinux, ...
  (thanks to all the packagers)

* Windows (32bit only)

* cpyext

  - C extension compatibility module

  - from "alpha" to "beta"

  - runs (big part of) **PyOpenSSL** and **lxml**

* py3k in progress

  - see later

  - 2.7 support never going away

PyPy organization
-----------------

* Part of Software Freedom Conservancy

  - Bradley successfully fighting U.S. bureaucracy

  - we are happy about it


* Funding model

  - py3k, numpy, STM

  - more than 100'000$ in donations

  - from individuals, large companies and the PSF

  - **thank to all**


Let's talk about Python
-----------------------

* Rapid prototyping

  - run your web server in 3 seconds

  - run your script in 0.1s

* Glue language

   - integrating with C is "easy"

Let's talk about PyPy
---------------------

* JIT warmup time

  - significant

  - rapid prototyping is harder

* no good way to call C from PyPy (yet)

JIT warmup times
----------------

* it's complicated

* we did not spend much time on that topic

* come and talk to us

XXX ask antonio if he can cover this on a jit talk

Py3k status
-----------

XXX write me

NumPy
-----

* progress going slowly

* multi dimensional arrays, broadcasting, fancy indexing

* all dtypes, except complex, strings and objects

* tons of functions missing

* you can help!

Calling C
---------

.. image:: standards.png

Calling C landscape
-------------------

* CPython C extensions

* SWIG, SIP, wrapper generators

* ctypes

* Cython

* CFFI (our new thing)

CFFI slide
----------

* XXX a bit of example code


STM
---

XXX
