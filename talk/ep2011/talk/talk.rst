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

* **MyHDL**: VHDL-like language written in Python

  - |scriptsize| http://www.myhdl.org/doku.php/performance |end_scriptsize|

  - (now) competitive with "real world" VHDL and Verilog simulators


|pause|

|example<| ``myhdl.org`` |>|
|small|

  [...] the results are spectacular. By simply using a different interpreter,
  our simulations run 6 to 12 times faster.

|end_small|
|end_example|



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


Why Python is slow?
-------------------

- Huge stack of layers over the bare metal

- Abstraction has a cost |pause| (... or not?) |pause|

- XXX: write a nice diagram showing how far is "a+b" from "add EAX, EBX" (or
  equivalent)


Killing the abstraction overhead
--------------------------------

|scriptsize|
|column1|
|example<| Python |>|

.. sourcecode:: python

    class Point(object):

      def __init__(self, x, y):
        self.x = x
        self.y = y

      def __add__(self, q):
        if not isinstance(q, Point):
            raise TypeError
        x1 = self.x + q.x
        y1 = self.y + q.y
        return Point(x1, y1)

    def main():
      p = Point(0.0, 0.0)
      while p.x < 2000.0:
        p = p + Point(1.0, 0.5)
      print p.x, p.y

|end_example|

|pause|

|column2|
|example<| C |>|

.. sourcecode:: c

   #include <stdio.h>







    

    int main() {
        float px = 0.0, py = 0.0;
        while (px < 2000.0) {
            px += 1.0;
            py += 0.5;
        }
        printf("%f %f\n", px, py);
    }

|end_example|
|end_columns|
|end_scriptsize|

.. at this point, we show it in the jitviewer

Useless optimization techniques
-------------------------------

.. XXX: I'm not sure how useful is this slide

|scriptsize|

|column1|
|example<| |>|

.. sourcecode:: python
   
   #
   for item in some_large_list:
       self.meth(item)

|end_example|
|column2|
|example<| |>|

.. sourcecode:: python

   meth = self.meth
   for item in some_large_list:
       meth(item)


|end_example|
|end_columns|

|pause|

|column1|
|example<| |>|

.. sourcecode:: python
   
   def foo():
       res = 0
       for item in some_large_list:
           res = res + abs(item)
       return res

|end_example|
|column2|
|example<| |>|

.. sourcecode:: python

   def foo(abs=abs):
       res = 0
       for item in some_large_list:
           res = res + abs(item)
       return res

|end_example|
|end_columns|

|pause|

|column1|
|example<| |>|

.. sourcecode:: python

   #

   [i**2 for i in range(100)]

|end_example|
|column2|
|example<| |>|

.. sourcecode:: python

   from itertools import *
   list(imap(pow, count(0), 
             repeat(2, 100)))

|end_example|
|end_columns|

|pause|

|column1|
|example<| |>|

.. sourcecode:: python

   for i in range(large_number):
       ...

|end_example|
|column2|
|example<| |>|

.. sourcecode:: python

   for i in xrange(large_number):
       ...

|end_example|
|end_columns|

|pause|

|column1|
|example<| |>|

.. sourcecode:: python

   class A(object):
       pass

|end_example|
|column2|
|example<| |>|

.. sourcecode:: python

   class A(object):
       __slots__ = ['a', 'b', 'c']

|end_example|
|end_columns|

|end_scriptsize|


Concrete example: ``ctypes``
----------------------------

|example<| |>|
|scriptsize|

.. sourcecode:: python

    import ctypes
    libm = ctypes.CDLL('libm.so')
    pow = libm.pow
    pow.argtypes = [ctypes.c_double, ctypes.c_double]
    pow.restype = ctypes.c_double

|end_scriptsize|
|end_example|

