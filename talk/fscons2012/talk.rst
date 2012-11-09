.. include:: beamerdefs.txt

============================================
Software Transactional Memory "for real"
============================================


Introduction
------------------

* This talk is about programming multi- or many-core machines


About myself
------------------

* Armin Rigo

* "Language implementation guy"

|pause|

* PyPy project

  - Python in Python

  - includes a Just-in-Time Compiler "Generator" for Python
    and any other dynamic language


Motivation
----------------------

* A single-core program is getting exponentially slower than a multi-core one

|pause|

* Using several processes exchanging data

  - works fine in some cases

  - but becomes a large mess in others

|pause|

* Using several threads

  - this talk!


Common solution
----------------------

* Organize your program in multiple threads

* Add synchronization when accessing shared, non-read-only data


Synchronization with locks
--------------------------

* Carefully place locks around every access to shared data

|pause|

* How do you know if you missed a place?

  - hard to catch by writing tests

  - instead you get obscure rare run-time crashes

|pause|

* Issues when scaling to a large program

  - order of acquisition

  - deadlocks


Synchronization with TM
-----------------------

* TM = Transactional Memory

|pause|

.. sourcecode:: plain

    ----------------   --------------------
    Locks              Transactional Memory
    ----------------   --------------------

    mylock.acquire();    atomic {
    x = list1.pop();       x = list1.pop();
    list2.append(x);       list2.append(x);
    mylock.release();    }


Locks versus TM
---------------

* Locks

.. image:: withlock.png
   :scale: 70%
   :align: center

* TM

.. image:: withstm0.png
   :scale: 70%
   :align: center


Locks versus TM
---------------

* Locks

.. image:: withlock.png
   :scale: 70%
   :align: center

* TM in case of conflict

.. image:: withstm.png
   :scale: 70%
   :align: center


Synchronization with TM
-----------------------

* "Optimistic" approach:

  - no lock to protect shared data in memory

  - instead, track all memory accesses

  - detect actual conflicts

  - if conflict, restart the whole "transaction"

|pause|

* Easier to use

  - no need to name locks

  - no deadlocks

  - "composability"


HTM versus STM
--------------

* HTM = Hardware Transactional Memory

  - Intel Haswell CPU, 2013

  - and others

|pause|

* STM = Software Transactional Memory

  - various approaches

  - large overhead (2x-10x), but getting faster

  - experimental in PyPy: read/write barriers, as with GC


The catch
---------

|pause|

* You Still Have To Use Threads

|pause|

* Threads are hard to debug, non-reproductible

|pause|

* Threads are Messy


Issue with threads
------------------

* TM does not solve this problem:

* How do you know if you missed a place to put ``atomic`` around?

  - hard to catch by writing tests

  - instead you get obscure rare run-time crashes

|pause|

* What if we put ``atomic`` everywhere?


Analogy with Garbage Collection
-------------------------------

* Explicit Memory Management:

  - messy, hard to debug rare leaks or corruptions

|pause|

* Automatic GC solves it

  - common languages either have a GC or not

  - if they have a GC, it controls almost *all* objects

  - not just a small part of them


Proposed solution
-----------------

* Put ``atomic`` everywhere...

* in other words, Run Everything with TM


Proposed solution
-----------------

* Really needs TM.  With locks, you'd get this:

.. image:: GIL.png
   :scale: 70%
   :align: center

* With TM you can get this:

.. image:: STM.png
   :scale: 70%
   :align: center


In a few words
--------------

* Longer transactions

* Corresponding to larger parts of the program

* The underlying multi-threaded model becomes implicit


Typical example
---------------

* You want to run ``f1()`` and ``f2()`` and ``f3()``

|pause|

* Assume they are "mostly independent"

  - i.e. we expect that we can run them in parallel

  - but we cannot prove it, we just hope that in the common case we can

|pause|

* In case of conflicts, we don't want random behavior

  - i.e. we don't want thread-like non-determinism and crashes


Pooling and atomic statements
-----------------------------

* Solution: use a library that creates a pool of threads

* Each thread picks a function from the list and runs it
  with ``atomic``


Results
-------

* The behavior is "as if" we had run ``f1()``, ``f2()``
  and ``f3()`` sequentially

* The programmer chooses if he wants this fixed order,
  or if any order is fine

* Threads are hidden from the programmer


More generally
--------------

* This was an example only

* **TM gives various new ways to hide threads under a nice interface**


Not the Ultimate Solution
-------------------------

* Much easier for the programmer to get reproducible results

* But maybe too many conflicts

|pause|

* "The right side" of the problem

  - start with a working program, and improve performance

  - as opposed to: with locks, start with a fast program, and debug crashes

  - we will need new debugging tools


PyPy-STM
--------

* PyPy-STM: a version of PyPy with Software Transactional Memory

  - in-progress, but basically working

* http://pypy.org/

|pause|

* Thank you!
