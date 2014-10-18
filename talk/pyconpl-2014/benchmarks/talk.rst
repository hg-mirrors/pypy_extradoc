---------------------
How to benchmark code
---------------------

Who are we?
------------

xxx

What is this talk is about?
---------------------------

* basics how CPython and PyPy run programs

* a bit of theory about measuring performance

* microbenchmarks

* complicated picture of "real world"

CPython
-------

* a "simple" virtual machine

* compiles python code to bytecode

* runs the bytecode

* usually invokes tons of runtime functions written in C

CPython (demo)
--------------

PyPy
----

* not so simple virtual machine

* all of the above

* ... and then if the loop/function gets called often enough
  it's compiled down to an optimized assembler by the JIT

PyPy (demo)
-----------

Measurments 101
---------------

* run your benchmark multiple times

* the distribution should be gaussian

* take the average and the variation

* if the variation is too large, increase the number of iterations

Let's do it (demo)
------------------

Problems
--------

* the whole previous slide is a bunch of nonsense

* ...

"Solution"
----------

* you try your best and do the average anyway

* presumably cutting off the warmup time

|pause|

* not ideal at all
