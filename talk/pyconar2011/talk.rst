.. include:: beamerdefs.txt

=============================
Making little things possible
=============================

Python
------

* Python is great

|pause|

* Python is a glue language

|pause|

* Python is slow

Is python slow?
---------------

.. image:: wikipedian_protester.png
   :scale: 500%
   :align: center

|small|

* http://blog.bossylobster.com/2011/08/lesson-v8-can-teach-python-and-other.html

|end_small|

* PyPy **29 wins**, Node.js (V8) **20 wins**, one tie

What is PyPy?
-------------

* PyPy is many things

* **just another python implementation**

.. sourcecode:: bash

  pypy x.py

What is PyPy (2)?
-----------------

* Comes with a JIT compiler

* Stackless

|pause|

* **fast**

How fast is PyPy?
-----------------

PyPy 1.6 - status
-----------------

* Released on 16th of August

* Python 2.7.1

* The most compatible alternative to CPython

* Most programs just work

* (C extensions might not)

PyPy 1.6 - status (2)
---------------------

* numpy (in progress)

* ctypes (fast)

* stable and compatible

PyPy 1.6 - what you can do
--------------------------

* try using on your own programs

* a lot of libraries just work

* your programs either no or minimal changes

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

How you can help?
-----------------

* Try it on your application

  - if it's slow, we want to know!

  - if it does not work, too :-)

  - if it works and it's fast, that as well

* Tell people about PyPy

* Contribute to PyPy! (it's not **that** hard :-))

Things you can do with Python using PyPy
----------------------------------------

|pause|

* real time video processing

|pause|

* software-rendered games

|pause|

* this is just the beginning!

Contacts, Q/A
--------------

- http://pypy.org

- blog: http://morepypy.blogspot.com

- mailing list: pypy-dev@python.org

- IRC: #pypy on freenode

.. image:: ../ep2011/talk/question-mark.png
   :scale: 10%
   :align: center

Shameless ad
------------

* Want to make run your software fast?

* We can make it happen

* fijall@gmail.com
