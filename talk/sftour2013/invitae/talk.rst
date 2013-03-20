.. include:: beamerdefs.txt

============================
Writing fast Python programs
============================

who we are
----------

* Maciej Fijałkowski

* Armin Rigo

what we're going to talk about
------------------------------

* the problem of fast python

* cython, numpy, weave, etc

* PyPy and our approach

* promise to keep it short

python language
---------------

* expressive

* concise

* performance characteristics not 100% clear

classic solutions
-----------------

* use numpy, but your algorithms have to be vectorized

|pause|

* use cython, but you have to write down your types

|pause|

* don't use python, just call C

demo
----

...

pypy approach
-------------

* make language fast enough for algorithms

* make numpy compatible enough to reuse it

* more algorithms less pipeline building

more
----

* pypy.org

