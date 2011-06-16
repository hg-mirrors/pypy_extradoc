.. include:: beamerdefs.txt

================================
PyPy in production
================================

What is PyPy?
-------------

|pause|

* Past EuroPython talks:

  - |scriptsize| **2004**: PyPy

  - **2005**: PyPy as a compiler

  - **2006**: An introduction to PyPy, PyPy architecture session, What can PyPy do for you

  - **2007**: PyPy 1.0 and Beyond, PyPy Python Interpreter(s) Features, PyPy: Why and
    how did it (not) work?

  - **2008**: PyPy for the rest of us, PyPy status talk

  - **2009** PyPy: Complete and Fast

  - **2010**: PyPy 1.3: Status and News |end_scriptsize|

|pause|

* You should know by now :-)

What is PyPy? (seriously)
-------------------------

* PyPy

  - started in 2003

  - Open Source, partially funded by EU and others

  - framework for fast dynamic languages

  - **Python implementation**

* as a Python dev, you care about the latter


PyPy 1.5
---------

* Released on 30 April, 2011

* Python 2.7.1

* The most compatible alternative to CPython

* Most programs just work

* (C extensions might not)

|pause|

* **fast**


PyPy features
---------------

* JIT

  - automatically generated

  - complete/correct by construction

  - multiple backends: x86-32, x86-64, ARM

|pause|

* Stackless

  - not yet integrated with the JIT (in-progress)

|pause|

* cpyext

  - CPython C-API compatibility layer

  - not always working

  - often working: wxPython, PIL, cx_Oracle, mysqldb, pycairo, ...

|pause|

* compact instances (as using ``__slots__``)


Speed
------

.. image:: pypy-vs-cpython.png
   :scale: 40%
   :align: center


Improvements in the past year
------------------------------

.. image:: django-last-year.png
   :scale: 38%
   :align: center


Compare to CPython
-------------------

.. image:: django-vs-cpython.png
   :scale: 38%
   :align: center


Real world use case (1)
-----------------------

* LWN's gitdm

  - http://lwn.net/Articles/442268/

  - data mining tool

  - reads the output of ``git log``

  - generate kernel development statistics

|pause|

* Performance

  - CPython: 63 seconds

  - PyPy: **21 seconds**

|pause|

|example<| ``lwn.net`` |>|
|small|

  [...] PyPy is ready for prime time; it implements the (Python 2.x)
  language faithfully, and it is fast.

|end_small|
|end_example|


Real world use case (2)
-----------------------

XXX write slide about this, the site is down ATM
http://www.myhdl.org/doku.php/performance


Real world use case (3)
-----------------------

- Translating PyPy itself

- Huge, complex piece of software

- All possible (and impossible :-)) kinds of dynamic and metaprogrammig tricks

- ~2.5x faster with PyPy

- (slow warm-up phase, though)

- Ouroboros! |snake|

Not convinced yet?
------------------

|example<| Real time edge detection |>|
|small|

.. sourcecode:: python

    def sobeldx(img):
      res = img.clone(typecode='d')
      for p in img.pixeliter():
          res[p] = (-1.0 * img[p + (-1,-1)] +
                     1.0 * img[p + ( 1,-1)] +
                    -2.0 * img[p + (-1, 0)] +
                     2.0 * img[p + ( 1, 0)] +
                    -1.0 * img[p + (-1, 1)] +
                     1.0 * img[p + ( 1, 1)]) / 4.0
      return res
    ...
    ...

|end_small|
|end_example|

Live demo
---------

.. image:: demo.png
   :scale: 38%
   :align: center



