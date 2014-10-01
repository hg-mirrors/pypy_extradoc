.. include:: beamerdefs.txt

PyPy : A fast Python Virtual Machine
====================================

Me
--

- rguillebert on twitter and irc

- PyPy contributor since 2011

- NumPyPy contributor

- Software consultant (hire me !)

- Feel free to interrupt

Introduction
------------

- "PyPy is a fast, compliant alternative implementation of the Python language"

- Aims to reach the best performance possible without changing the syntax or semantics

- Supports x86, x86_64, ARM

- Production ready

- MIT Licensed

Speed
-----

.. image:: speed.png
   :scale: 37%

Speed
-----

- Automatically generated tracing just-in-time compiler

- Generates efficient machine code based on runtime observations

- Removes overhead when unnecessary

- But these Python features remain available (pdb)

RPython
-------

- Subset of Python

- Made for writting virtual machines

- Takes care of garbage collection and JIT compilation

- A VM written in RPython doesn't have to know about the garbage collector

- Minimal help from the VM is needed in order to have an efficient JIT (a few annotations)

Demo
----

- Real-time edge detection

How
---

- Removes boxing, integer objects become machine integers

- Specializes trace on types, helps speed-up method lookup

- If the type of the object is different from the type in the trace, go back to the interpreter : "guard failure"

- If a guard fails too many times, generate traces for the other types frequently encountered

Compatibility
-------------

- Fully compatible with CPython 2.7 & 3.2 (minus bugs & implementation specific features)

- Partial and slow support of the C-API

- Alternatives might exist

Ecosystem
---------

- Just my opinion

- We should move away from the C-API

  * Makes assumptions on refcounting, object layout, the GIL

  * The future of Python is bound to the future of CPython (a more than 20 years old interpreter)

  * It's hard for a new Python VM without C extension support to get traction (not only PyPy)

- This doesn't mean we should lose Python's ability to interface with C easily

CFFI
----

- Where do we go from here ?

- CFFI is a fairly new way of interacting with C in an implementation independant way

- Very fast on PyPy

- Decently fast on CPython

- The Jython project is working on fast support

CFFI
----

- More convenient, safer, faster than ctypes

- Python functions can be exposed to C easily

- Already used by pyopenssl, psycopg2cffi, pygame_cffi, lxml_cffi

- Other tools could be built on top of it (Cython cffi backend ?)
