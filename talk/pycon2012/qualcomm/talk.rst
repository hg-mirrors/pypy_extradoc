
.. include:: ../tutorial/beamerdefs.txt

===============================
Building interpreters with PyPy
===============================

What is PyPy?
=============

* a fast Python interpreter with a JIT

* **a framework to write dynamic language interpreters**

* an open source project on the BSD license

* an agile project with contributors from all over the world

A bit about the architecture
============================

* describe your VM in a **high level language**

* implement your object model, types etc.

* you get a **GC** and **JIT** for free

|pause|

* with a few hints for the JIT

PyPy's architecture
===================

* RPython program, imported and initialized

* transformed to control flow graphs

* compiled do C -OR- JVM -OR- graphs for JIT

* this is a very high-level overview

JIT architecture
================

* works on the level of the **interpreter**

* by design complete

* from a single source code of the **interpreter**

Links
=====

* morepypy.blogspot.com

* doc.pypy.org

* #pypy on freenode

