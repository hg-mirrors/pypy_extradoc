Software Transactional Memory with PyPy
=======================================

Description
-----------

PyPy is a fast alternative Python implementation.  Software
Transactional Memory is a current academic research topic.  Put the two
together --brew for a couple of years-- and we obtain a version of PyPy
that runs on multiple cores, without the infamous Global Interpreter
Lock (GIL).  It has been released last year in beta, including
integration with the Just-in-Time compiler.


Audience
--------

People interested in PyPy; people looking for concurrency solutions.


Objectives
----------

Attendees will learn about a way to use multiple cores in their
applications, and how it differs from the 'multiprocessing' package.


Detailed abstract
-----------------

A special version of PyPy runs on multiple cores, without the infamous
Global Interpreter Lock (GIL).  It means it can run a single program
using multiple cores, rather than being limited to one core, like it
is the case for CPU-intensive programs on CPython.

But the point is not only that: it can give the illusion of
single-threaded programming, even when you really want the program to
use multiple cores.  I will give examples of what I mean exactly by
that.  Starting from the usual multithreaded demos --with explicit
threads-- I will move to other examples where the actual threads are
hidden to the programmer.  I will explain how we can modify/have
modified the core of async libraries (Twisted, Tornado, gevent, ...) to
use multiples threads, without exposing any concurrency issues to the
user of the library --- the existing Twisted/etc. programs still run
mostly without change.  Depending on the status at the time of the
presentation, I will give demos of this, explaining in detail what
people can expect to have to change (very little), and how it performs
on real applications.

I will give a comparison with the alternatives, foremost of which is the
stdlib 'multiprocessing' package.

I will also give an overview of how things work under the cover: the
10000-feet view is to create internally copies of objects and write
changes into these copies.  This allows the originals to continue being
used by other threads.  It is an adaptation of previous work on
Software Transactional Memory (STM), notably RSTM.


Outline
-------

1. Intro (5 min): PyPy, STM

2. Examples and demos (10 min): simple multithreading; atomic
   multithreading; Twisted/etc. model; performance numbers.

3. Comparison (5 min): independent processes; multiprocessing; custom
   solutions.

4. How things work under the cover (5 min): overview.


Additional notes
----------------

* Follow the progress of STM in PyPy:
  http://morepypy.blogspot.ch/search/label/stm
