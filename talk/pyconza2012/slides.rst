==================================
Python performance characteristics
==================================

Who am I?
---------

* Maciej Fijałkowski (yes this is unicode)

* PyPy core developer for I don't remember

* performance freak

What this talk is about?
------------------------

* I'll start where Larry finished

* describe a bit how the PyPy JIT works

* what's the difference between interpretation and JIT compilation

|pause|

* show some assembler

|pause|

* just joking

Disclaimer
----------

* we're trying to make it better

What is PyPy?
-------------

* PyPy is a Python interpreter (that's what we care about)

* PyPy is a toolchain for creating dynamic language implementations

  * we try to rename the latter RPython

* also, an Open Source project that has been around for a while

Compilers vs interpreters
-------------------------

* compilers compile language X (C, Python) to a lower level language
  (C, assembler) ahead of time

* interpreters compile language X to bytecode and have a big interpreter
  loop

|pause|

* PyPy has a hybrid approach. It's an interpreter, but hot paths are
  compiled directly to assembler during runtime

What is just in time (JIT) compilation?
---------------------------------------

* few different flavors

* observe runtime values

* compile code with agressive optimizations

* have checks if assumptions still stand

So what PyPy does?
------------------

* interprets a Python program

* the JIT observes python **interpreter**

* producing code through the path followed by the interpreter

* compiles loops and functions

Some example
------------

* integer addition!

So wait, where are those allocations?
-------------------------------------

* they don't escape, so they're removed!

Abstractions
------------

* inlining, malloc removal

* abstractions are cheap

|pause|

* if they don't introduce too much complexity

Allocations
-----------

* allocation is expensive

* for a good GC, short living objects don't matter

* it's better to have a small persistent structure and abstraction
  on allocation

|pause|

* copying however is expensive

* we have hacks for strings, but they're not complete

Calls
-----

* Python calls are an incredible mess

* simple is better than complex

* simple call comes with no cost, the cost grows with growing complexity

Attribute access
----------------

* if optimized, almost as fast as local var access

* ``dict`` lookup optimized away

* class attributes considered constant

* meta programming is better than dynamism

* objects for small number of constant keys, dicts for large
  numbers of changing keys

Other sorts of loops
--------------------

* there is more!

* ``tuple(iterable)``, ``map(iterable)``, ``re.search``

* they're all jitted

* not all nicely

Future improvements
-------------------

Xxxx
