Python & PyPy performance (not) for dummies
-------------------------------------------

In this talk we would like to talk a bit about the performance
characteristics of python programs, how to (or when not to) write benchmarks
and how to measure performance of the existing python programs both
under CPython (the standard python interpreter) and PyPy.

One of the key points will be presentation of vmprof, a low-overhead
Python statistical profiler written by us.

The talk will cover:

* the basics of statistics and benchmarking

* tools available for measuring the performance of python programs

* common strategies to improve the bottlenecks

About author:
-------------

Maciej is a freelancer working mostly on PyPy for the past several
years. He's a core developer since 2006, working on all kinds of parts
in the entire codebase including JIT, GC and assembler
backends. Maciej has been going to many conferences, advertising PyPy
to a broader audience for the past several years, including a keynote
at Pycon 2010. He's also the main maintainer of jitviewer and vmprof, tools
analyzing performance of your python programs under PyPy.
