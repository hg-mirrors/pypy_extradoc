.. include:: beamerdefs.txt

================================
PyPy training session
================================

PyPy training session
---------------------

- Part 1: Run your application under PyPy

- Part 2: Write your own interpreter with PyPy


Part 1
------

* Run your application under PyPy


How to run PyPy
----------------

* ``pypy program.py``

* That's it!


Refcounting vs generational GC (1)
----------------------------------

|scriptsize|
|example<| |scriptsize| ``gc0.py`` |end_scriptsize| |>|

.. sourcecode:: python

   def foo():
       f = file('/tmp/bar.txt', 'w')
       f.write('hello world')

   foo()
   print file('/tmp/bar.txt').read()

|end_example|

|pause|
|example<| |scriptsize| ``gc1.py`` |end_scriptsize| |>|

.. sourcecode:: python

   def foo():
       f = file('/tmp/bar.txt', 'w')
       f.write('hello world')
       f.close() # <-------

|end_example|

|pause|
|example<| |scriptsize| ``gc2.py`` |end_scriptsize| |>|

.. sourcecode:: python

   def foo():
       with file('/tmp/bar.txt', 'w') as f:
           f.write('hello world')

|end_example|
|end_scriptsize|


Refcounting vs generational GC (2)
----------------------------------

* ``__del__``

  - especially files or sockets

  - don't leak file descriptors!

* weakrefs

* ``finally`` inside generators

Challenge
---------

- Find the bug!

XXX write me :-(


How the JIT works
-----------------------

XXX write me


PYPYLOG
--------

* ``PYPYLOG=categories:logfile pypy program.py``

* categories:

  - gc

  - jit-log-noopt, jit-log-opt

  - jit-backend

  - jit-backend-counts

* ``PYPYLOG=jit-log-opt:log.pypylog pypy foo.py``

XXX: write foo.py


The jitviewer
-------------

- ``jitviewer.py log.pypylog``
