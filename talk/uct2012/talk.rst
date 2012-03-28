Fast enough VMs in fast enough time
===================================

Who am I?
---------

* PyPy developer since 2006

XXX

What is PyPy?
-------------

* an open source project

* a Python interpreter

* **a framework for writing dynamic language VMs**

* an agile project sponsored by EU and others

What is a VM?
-------------

* a program

* input: a program

* output: the result of executing that program

What does a VM look like?
-------------------------

* Lexical/analysis parsing (what are the symbols in the program)

* AST construction (what is the structure of the program)

* Bytecode compilation (optional)

* Execution

Where does PyPy come in?
------------------------

* Tools for writing these program quickly, and efficiently.

  * Helpers for things like parsing

  * Free JIT, and garbage collector

* Mostly you write a totally normal VM in python, and it becomes magically fast

PyPy architecture
-----------------

* snakes all the way down

* everything is written in Python - including JIT, GC, etc.

* to be precise, a **subset** of Python, called RPython

* your VM has to be implemented in RPython

RPython - the good
------------------

* The good - it's mostly Python

* Just write python and fix it later

RPython - the bad
-----------------

* It's restricted

* Most dynamic features don't work, but you can employ all kinds of tricks during import

RPython - the ugly
-------------------

* Documentation

* Error messages

* Global type inference
