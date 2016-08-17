.. include:: ../beamerdefs.txt

---------------------
How to benchmark code
---------------------

Who are we?
------------

* Maciej Fijalkowski, Armin Rigo

* working on PyPy

* interested in performance

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

Writing benchmarks - typical approach
-------------------------------------

* write a set of small programs that exercise one particular thing

  * recursive fibonacci

  * pybench

PyBench
-------

* used to be a tool to compare python implementations

* only uses microbenchmarks

* assumes operation times are concatenative

Problems
--------

* a lot of effects are not concatenative

* optimizations often collapse consecutive operations

* large scale effects only show up on large programs

An example
----------

* python 2.6 vs python 2.7 had minimal performance changes

* somewhere in the changelog, there is a gc change mentioned

* it made pypy translation toolchain jump from 3h to 1h

* it's "impossible" to write a microbenchmarks for this

More problems
-------------

* half of the blog posts comparing VM performance uses recursive fibonacci

* most of the others use computer language shootout

PyPy benchmark suite
--------------------

* programs from small to medium and large

* 50 LOC to 100k LOC

* try to exercise various parts of language (but e.g. lack IO)

Solutions
---------

* measure what you are really interested in

* derive microbenchmarks from your bottlenecks

* be skeptical

* understand what you're measuring

Q&A
---

- http://pypy.org/

- http://morepypy.blogspot.com/

- http://baroquesoftware.com/

- ``#pypy`` at freenode.net

- Any question?

