==========================================================
Using All These Cores: Transactional Memory under the hood
==========================================================


.. summary:
    - Intro
    - Using multiple threads: C++, Java; Jython, IronPython
    - the GIL in CPython
    - "bytecode" is uninteresting for the Python programmer
    - but larger blocks are
    - if we can make these larger blocks atomic, we win
    - "with atomic:"
    - theoretical only so far!
    - best example: event-driven *non-multithreaded* systems
    - under the hood: transactional memory


Introduction
============

* Armin Rigo

* PyPy dev, CPython dev


Problem
=======

* Most computer's CPUs today have multiple cores

* How to use them?


Multithread programming
=======================

* C, C++, Java, .NET, ...

* Jython, IronPython


CPython, PyPy
=============

* No story so far

* Alternatives for various cases

* Some fine and some horrible


The GIL
=======

* Global Interpreter Lock

* "Each bytecode is executed atomically"


Transactional Memory
====================

* Recent research

* Optimistically runs multiple threads even if they
  are supposed to be waiting on the same lock

* High overheads (but working on it)


Expected results
================

* Runs multiple threads despite having a single GIL

* Does not remove the GIL, but solves the original problem anyway


Kinds of Transactional Memory
=============================

* STM: Software Transactional Memory

* HTM: Hardware Transactional Memory

* Hybrids


Status
======

* STM is still at least 2x slower (speed on a single core)

* HTM in Ruby with Intel Haswell CPUs: not bad but
  still disappointing (imo)


STM C7
======

* Our group's research

* Hope: much less than 2x slower for "PyPy-like" usages

* (insert description here)


Atomic sections
===============

* GIL = "each bytecode is atomic"

* One bytecode?  Obscure for the regular Python programmer

* Larger atomic sections: ``with atomic:``


So...
=====

* New way to synchronize multiple threads: ``with atomic:``

* All ``atomic`` blocks appear to run serialized

* With STM/HTM, they actually run in parallel as far as possible


No threads?
===========

* Works even if you don't use threads!

* If the Twisted reactor was modified to start a pool of threads,
  and to run all events in ``with atomic:``

* ...Then the end result is the same, for any Twisted program


Behind-the-scene threads
========================

* The thread pool added behind the scene lets a STM/HTM-enabled
  Python run on several cores

* The ``with atomic:`` means that the semantics of the Twisted
  program didn't change


Summary (optimistic)
====================

* If you are a Twisted developer...

* Just wait and your program will run on multiple cores ``:-)``


Conflicts
=========

* Actually, your program will likely fail to use multiple cores
  out of the box

* ...Because of "conflicts": each event should be "often" independent,
  but may not be (e.g. because they each incrementing a global counter
  or similar)


Some work left for you to do
============================

* You need to figure out where the conficts are

* Maybe using some debugger-like tool that reports conflicts

* Then you need small rewrites to avoid them


What is the point?
==================

* The point is that with STM/HTM your program is always *correct*
  (as much as the single-core version is)

* You need to work in order to fix the most obvious conflicts

* If you don't, it won't be faster than the single-core original


What did we win?
================

* Regular approach to multithreading: your program is always *fast*

* You need to work in order to fix the bugs (races, deadlocks...)

* You need to find and fix *all* bugs -- as opposed to the STM/HTM
  version where you only fix *some* issues until it is fast enough


Scope
=====

* Twisted / Eventlet / Stackless / etc.: event-driven programming

* Any program computing something complicated, e.g. over all items in
  a dictionary, occasionally updating a shared state, etc.

* In general, any CPU-bound program with identifiable sections that
  have a good chance to be parallelizable: "a good chance" is enough


Conclusion
==========

* Mostly theoretical for now: there is a risk it won't work in
  practice (I bet it will ``:-)``)

* Expect progress in the following months: http://morepypy.blogspot.com/
