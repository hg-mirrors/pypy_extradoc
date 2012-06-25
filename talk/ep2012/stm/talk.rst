
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

* PyPy has been around since 2003

* first production ready (as advertised) release in December 2010 (1.4)

* funded from various sources, including EU FP6 programme

Current status
--------------

* release 1.9, **1.7x** faster than 1.5 (a year ago),
  **2.2x** faster than 1.4, **5.5x** faster than CPython

* more importantly, the range of programs PyPy can speed up has improved
  greatly

* implements 2.7.2 Python

* packaging: Debian, Ubuntu, Fedora, Homebrew, Gentoo, ArchLinux, ...
  (thanks to all the packagers)

* windows (but still 32bit binary only)

* cpython C extension compatibility module (cpyext)
  moved from 'alpha' to 'beta': it runs e.g. a big part of
  **PyOpenSSL** and **lxml**

PyPy organization
-----------------

* we joined the Software Freedom Conservancy
  (Bradley successfully fighting U.S. bureaucracy) and
  are happy about it

* funding: new model, more than 100'000$ in donations,
  both from a large number of individuals and a few large companies
  and the Python Software Foundation

Let's talk about Python
-----------------------

* rapid prototyping, run your web server in 3 seconds, run
  your script in 0.1s

* Python is very successful as a glue language - integrating
  with C is "easy"

Let's talk about PyPy
---------------------

* JIT warmup times are significant, making rapid prototyping
  harder

* we yet need to have a good way to call C from PyPy

JIT warmup times
----------------

* it's complicated

* we did not spend much time on that topic

* come and talk to us

XXX ask antonio if he can cover this on a jit talk

Calling C
---------

XXX xkcd 927 (google: xkcd standards)


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

NumPy
-----

XXX

STM
---

XXX
