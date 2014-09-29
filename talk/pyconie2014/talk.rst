.. include:: beamerdefs.tx

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

- If a guard fails too many times, optimize the trace for the other types frequently encountered
