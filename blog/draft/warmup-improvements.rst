Hello everyone!

I'm very pleased to announce that we've just managed to merge
the optresult branch.
Under this cryptic name is the biggest JIT refactoring we've done in a couple
years, mostly focused on the warmup time and memory impact of PyPy.

To understand why we did that, let's look back in time - back when we
got the first working JIT prototype in 2009 we were focused exclusively
on achieving peak performance with some consideration towards memory usage, but
without serious consideration towards warmup time. This means we accumulated
quite a bit of technical debt over time that we're trying, with difficulty,
to address right now. This branch mostly does not affect the peak performance
- it should however help you with short-living scripts, like test runs.

To see how much of a problem warmup is for your program, you can run your
program with ``PYPYLOG=jit-summary:-`` environment variable set.
This should show you something like this::

    (pypy-optresult)fijal@hermann:~/src/botbot-web$ PYPYLOG=jit-summary:- python orm.py 1500
    [d195a2fcecc] {jit-summary
    Tracing:      	781	2.924965
    Backend:      	737	0.722710
    TOTAL:      		35.912011
    ops:             	1860596
    recorded ops:    	493138
      calls:         	81022
    guards:          	131238
    opt ops:         	137263
    opt guards:      	35166
    forcings:        	4196
    abort: trace too long:	22
    abort: compiling:	0
    abort: vable escape:	22
    abort: bad loop: 	0
    abort: force quasi-immut:	0
    nvirtuals:       	183672
    nvholes:         	25797
    nvreused:        	116131
    Total # of loops:	193
    Total # of bridges:	575
    Freed # of loops:	6
    Freed # of bridges:	75
    [d195a48de18] jit-summary}

This means that the total (wall clock) time was 35.9s, out of which we spent
2.9s tracing 781 loops and 0.72s compiling them. The remaining couple were
aborted (trace too long is normal, vable escape means someone called
``sys._getframe()`` or equivalent). You can do the following things:

* compare the numbers with ``pypy --jit off`` and see at which number of
  iterations ``pypy`` jit kicks in

* play with the thresholds:
  ``pypy --jit threshold=500,function_threshold=400,trace_eagerness=50`` was
  much better in this example. What this does is to lower the threshold
  for tracing loops from default of 1039 to 400, threshold for tracing
  functions from the start from 1619 to 500 and threshold for tracing bridges
  from 200 to 50. Bridges are "alternative paths" that JIT did not take that
  are being additionally traced. We believe in sane defaults, so we'll try
  to improve upon those numbers, but generally speaking there is no one-size
  fits all here.

* if the tracing/backend time stays high, come and complain to us with
  benchmarks, we'll try to look at them


The branch does "one" thing - it changes the underlying model of how operations
are represented during tracing and optimizations. Let's consider a simple
loop like::

    [i0, i1]
    i2 = int_add(i0, i1)
    i3 = int_add(i2, 1)
    i4 = int_is_true(i3)
    guard_true(i4)
    jump(i3, i2)

The original representation would allocate a ``Box`` for each of ``i0`` - ``i4``
and then store those boxes in instances of ``ResOperation``. The list of such
operations would then go to the optimizer. Those lists are big - we usually
remove ``90%`` of them during optimizations, but they can be a couple thousand
elements. Overall, allocating those big lists takes a toll on warmup time,
especially due to the GC pressure. The branch removes the existance of ``Box``
completely, instead using a link to ``ResOperation`` itself. So say in the above
example, ``i2`` would refer to its producer - ``i2 = int_add(i0, i1)`` with
arguments getting special treatment.

That alone reduces the GC pressure slightly, but a reduced number
of instances also lets us store references on them directly instead
of going through expensive dictionaries, which were used to store optimizing
information about the boxes. Overall
we measured about 50% speed improvement in the optimizer, which reduces
the overall warmup time between 10% and 30%. The very
`obvious warmup benchmark`_ got a speedup from 4.5s to 3.5s, almost
30% improvement. Obviously the speedups on benchmarks would vastly
depend on how much warmup time is there in those benchmarks. We observed
annotation of pypy to decreasing by about 30% and the overall translation
time by about 7%, so your mileage may vary.

Of course, as usual with the large refactoring of a crucial piece of PyPy,
there are expected to be bugs. We are going to wait for the default branch
to stabilize
so you should see warmup improvements in the next release. If you're not afraid
to try, `nightlies`_ will already have them.

.. _`obvious warmup benchmark`: https://bitbucket.org/pypy/benchmarks/src/fe2e89c0ae6846e3a8d4142106a4857e95f17da7/warmup/function_call2.py?at=default
.. _`nightlies`: http://buildbot.pypy.org/nightly/trunk

Cheers!
fijal & arigo

