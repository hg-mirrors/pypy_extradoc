The PyPy project
================

What is this talk about?
------------------------

* short introduction to the PyPy project

* short introduction to RPython

* just in time compilation and other innovations

* how virtual machines should be written

* commercial vs open source (???)

Who am I?
---------

* Maciej Fijałkowski

* PyPy core developer

* own company - baroquesoftware.com

What's PyPy?
------------

* a python interpreter

* implements the full language (no restrictions!)

* runs faster

What makes PyPy different?
--------------------------

* not written in C/C++

* has just in time compiler

* runs fast

* core interpreter does not know about the JIT (mostly)

What's RPython?
---------------

* implementation language for PyPy (and other projects, topaz, hippyvm, ...)

* a subset of Python that can be statically compiled

* extensive static analysis and transformation (GC, JIT, ...)

RPython example
---------------

* demo

* like python, but can compile to C

* quite a bit quicker

RPython interpreter example
---------------------------

* RPython is an ugly language

* mostly for writing interpreters

* demo

Classic compilation
-------------------

* you take a language X, parse it, compile it to assembler

* works well for simple "static enough" languages

Virtual Machine
---------------

* you take language X, compile it to imaginary computer

* you implement that imaginary computer

JIT - introduction
------------------

* you have a virtual machine from the previous slide

* you compile bits and pieces of the code straight into assembler

Tracing JIT - introduction
--------------------------

* instead of compiling e.g. function at a time you **trace**
  what the interpreter does

* follow steps one by one and generate assembler

* very natural inlining, hot paths etc.

Metatracing
-----------

* trace the **interpreter** instead of the program

* for complicated languages, like Python, is essential

* hints necessary to close the semantics gap

* avoids duplication of code

RPython interpreter example - JIT
---------------------------------

* demo

* jit adding means adding a few hints (pypy has about 100)

Recap on virtual machines
-------------------------

* don't write virtual machines by hand

* don't write JITs in hand

* use tools (PyPy/truffle)

Q&A
---

* pypy.org

* baroquesoftware.com

* fijal@baroquesoftware.com

* Any questions?

Extra slide - what do I do for a living?
----------------------------------------

* selling pypy commercial support

* various grants

* implementing extra features
