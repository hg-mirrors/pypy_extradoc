=========================================
Why is Python slow and how PyPy can help?
=========================================

What's this talk about?
-----------------------

* short introduction to JITting

* how does a tracing JIT work

* semantics that make Python slow/hard to optimize
XXX cross slow

Short introduction to JITting
-----------------------------

* run code with the interpreter

* observe what it does

* generate optimized machine code for commonly executed paths

* using runtime knowledge (types, paths taken)

Tracing JIT
-----------

* compiles one loop at a time

* generates linear code paths, recording what the interpreter did

* for each possible branch, generate a guard, that exits assembler on triggering

* if guard fails often enough, start tracing from the failure

Tracing example
---------------

* we have cool tools!

XXX pic

Part 2 - python semantics
--------------------------

* we're going to concentrate on a few really annoying things

* frame introspection

* dynamic dispatch

* boxing

* dynamic method lookup

* attribute access

Dynamic dispatch
----------------

* each operation has to dispatch on the type of the first argument

* ``a + b`` can call integer addition, string concatenation or custom
  ``__add__`` method

* not much to talk about, tracing JIT deals with this without
  extra effort

* it can get fairly complex (XXX http://hg.python.org/cpython/file/6910af7df354/Objects/abstract.c#l761)

* all of this logic is constant folded (XXX trace)

Boxing
------

* for dynamic dispatch to work, each object has to be packed in a box

* ``PyIntObject``, ``PyFloatObject`` etc.

* it's wasteful, because it requires memory allocations (or pooling)

* ideally we would not allocate them unless they escape

* frames get in the way (they escape locals and valuestack)

XXX more traces

Frame introspection
-------------------

* ``sys._getframe()``, ``sys.exc_info()`` has to work

* require creating python frames on the heap

* not very convinient for fast access or escape analysis


Frame introspection - solution
------------------------------

* so called "virtualizables"

* frames are allocated and unpacked on processor (C) stack

* in case of frame introspection happening, JIT knows where to find necessary values

* reconstructed frame looks like it has always been there

Attribute access
----------------

* ``obj.attr``

* Look for ``__getattribute__`` on ``obj``

* check ``type(obj).__dict__`` for a descriptor

* check ``obj.__dict__`` for a value

* 3 dict lookups

Map dicts
-------------

* for a common case reduces 3 dict lookups to a list lookup

* makes objects very compact (same as with ``__slots__``)

* works even for adding attributes later on, after ``__init__``

Map dicts - how it works
-------------------------

* stores a structure remembering common object shapes

* a dictionary mapping names to numbers in a list

* a list per object

* those dictionary lookups are constant-folded away at the
  time of JIT compilation

XXX cool pics

Dynamic method lookup
---------------------

* ``obj.meth()``, what happens?

* 2 parts: attribute lookup, and method call

* check ``__dict__`` of ``obj`` and ``type(obj)`` (and the entire MRO)

* allocate a bound method

* call the bound method

Linking it all together
-----------------------

* array example

Things we did not talk about
----------------------------

* regular expressions

* generators

* recursion

* ``map`` and other looping constructs

Future directions
-----------------

* fast ctypes

* numpy

Thank you
-----------

* http://pypy.org

* http://morepypy.blogspot.com/
