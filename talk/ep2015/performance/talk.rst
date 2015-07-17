.. include:: beamerdefs.txt

==========================
Python & PyPy performance
==========================

About us
---------

- PyPy core devs

- ``pdb++``, ``fancycompleter``, ...

- Consultant

- http://baroquesoftware.com/


About you
-------------

- Target audience

- Your Python program is slow

- You want to make it fast(er)


Optimization for dummies
-------------------------

* Obligatory citation

  - *premature optimization is the root of all evil* (D. Knuth)

* Pareto principle, or 80-20 rule

  - 80% of the time will be spent in 20% of the program

* Two golden rules:

  1. Identify the slow spots

  2. Optimize them


This talk
----------------------------

* Two parts

  1. PyPy as a tool to make Python faster

  2. How to identify the slow spots



Tools
------

- Endless list of tools/techniques to increment speed

- C extension

- Cython

- numba

- "performance tricks"

- **PyPy**

  * We'll concentrate on it

  * WARNING: we wrote it, we are biased :)



What is PyPy
---------------

- Alternative, fast Python implementation

- Performance: JIT compiler, advanced GC

- PyPy 2.6.0 (Python version 2.7.9)

- Py3k as usual in progress (3.2.5 out, 3.3 in development)

- http://pypy.org

- EP Talks:
  
  * The GIL is dead: PyPy-STM
    
    (July 23, 16:45 by Armin Rigo)

  * PyPy ecosystem: CFFI, numpy, scipy, etc 
    
    (July 24, 15:15 by Romain Guillebert)


Speed: 7x faster than CPython
-------------------------------

.. image:: speed.png
   :scale: 47%


The JIT
--------

.. image:: jit-overview1.pdf
   :scale: 50%


The JIT
--------

.. image:: jit-overview2.pdf
   :scale: 50%


The JIT
--------

.. image:: jit-overview3.pdf
   :scale: 50%


JIT overview
-------------

- Tracing JIT

  * detect and compile "hot" loops

  * (although not only loops)

- **Specialization**

- Precompute as much as possible

- Constant propagation

- Aggressive inlining


Specialization (1)
-------------------

- ``obj.foo()``

- which code is executed? (SIMPLIFIED)

  * lookup ``foo`` in obj.__dict__

  * lookup ``foo`` in obj.__class__

  * lookup ``foo`` in obj.__bases__[0], etc.

  * finally, execute ``foo``

- without JIT, you need to do these steps again and again

- Precompute the lookup?


Specialization (2)
--------------------

- pretend and assume that ``obj.__class__`` IS constant

  * "promotion"

- guard

  * check our assumption: if it's false, bail out

- now we can directly jump to ``foo`` code

  * ...unless ``foo`` is in ``obj.__dict__``: GUARD!

  * ...unless ``foo.__class__.__dict__`` changed: GUARD!

- Too many guard failures?

  * Compile some more assembler!

- guards are cheap

  * out-of-line guards even more


Specialization (3)
---------------------

- who decides what to promote/specialize for?

  * we, the PyPy devs :)

  * heuristics

- instance attributes are never promoted

- class attributes are promoted by default (with some exceptions)

- module attributes (i.e., globals) as well

- bytecode constants


Specialization trade-offs
--------------------------

- Too much specialization

  * guards fails often

  * explosion of assembler

- Not enough specialization

  * inefficient code


Part 2
-------

* Measure performance

* Identify problems


What is performance?
--------------------

* it's a metric

* usually, time spent doing task X

* sometimes number of requests, latency, etc.

* some statistical properties about that metric (average, minimum, maximum)

Do you have a performance problem?
----------------------------------

* define the metric

* measure it (production, benchmarks, etc.)

* see if Python is the cause here (if it's not, we can't help you,
  but I'm sure someone help)

* make sure you can change and test stuff quickly (e.g. benchmarks are better
  than changing stuff in production)

We have a python problem
------------------------

* tools, timers etc.

* systems are too complicated to **guess** which will be faster

* find your bottlenecks

* 20/80 (but 20% of million lines is 200 000 lines, remember that)

Profilers landscape
-------------------

* cProfile, runSnakeRun (high overhead) - exact profiler

* plop, vmprof - statistical profiler

* cProfile & vmprof work on pypy

vmprof
------

XXXxxx

using vmprof
------------

yyyyyyy

interpreting the results
------------------------

xxxx

using vmprof in production
--------------------------

demo
----

let's optimize some code
------------------------

let's optimize some more complex code
-------------------------------------

Extras: what's cool what's not cool on cpython and pypy

CPython vs PyPy
---------------

* very different performance characteristics

* XXX list them

