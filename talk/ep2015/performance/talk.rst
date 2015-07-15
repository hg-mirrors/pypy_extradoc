
Python & PyPy performance
-------------------------

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

