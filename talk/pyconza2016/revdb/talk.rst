=========================
RevDB, a reverse debugger
=========================


Demo
===========================

.. raw:: latex

    \ 


How is that possible??
======================

* I did not cheat

* It really works for large programs


Main features
=============

* Travel in time: next/bnext, step/bstep, continue/bcontinue,
  finish/bfinish

* p expression-or-statement

* watch expression, break function/file:line, delete


On bigger programs
==================

* Write down what occurs at which time, because you're going
  to go back and forth until you are lost

* See ``help`` for all commands


Completeness
============

* Run any Python code that PyPy can also run: OK

* Multithread apps: OK

* CPython C extension modules: OK


Completeness
============

* Long-running programs: NO

* Stackless/greenlet/gevent: NO

* Track multiple processes: NO

* Windows: NO

* Python 3: NO (soon?)


Comparison
==========

* "Reverse debugging" == "Omniscient debugging" == "Historial debugging"
  == "Backwards debugging"

* for the C language: undodb-gdb, rr

* for Python (but not really the same thing): epdb, pode


Why not well-known?
===================

* It is often a cannon to take down a fly

* Performance issues: unlike gdb and pdb, they slow down normal
  execution (with some of them, massively)


Why not well-known?
===================

* They tend to crash

* Not all give a full, reliable history: sometimes you need to guess if
  the debugger is telling you lies

* Often proprietary software with restrictive licenses


Sometimes you need the cannon
=============================

* In a very complex piece of code, you will one day (or had to) hunt for
  a week for *one* bug

* I made RevDB in two months instead of spending one week tracking down a
  bug ``:-)``


Q & A
=====

https://bitbucket.org/pypy/revdb/
