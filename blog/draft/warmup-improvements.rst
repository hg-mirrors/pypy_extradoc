Hello everyone!

I'm very pleased to announce that we've just managed to merge
the optresult branch.
Under this cryptic name is the biggest JIT refactoring we've done in a couple
years, mostly focused on the warmup time and memory impact of PyPy.

To understand why we did that, let's look back in time - back when we
got the first working JIT prototype in 2009 we were focused exclusively
on the peak performance with some consideration towards memory usage, but
without serious consideration towards warmup time. This means we accumulated
quite a bit of technical debt over time that we're trying, with difficulty,
to address right now. This branch mostly does not affect the peak performance
- it should however help you with short-living scripts, like test runs.

The branch does "one" thing - it changes the underlaying model of how operations
are represented during the tracing and optimizations. Let's consider a simple
loop like that::

    [i0, i1]
    i2 = int_add(i0, i1)
    i3 = int_add(i2, 1)
    i4 = int_is_true(i3)
    guard_true(i4)
    jump(i3, i2)

The original representation would allocate a ``Box`` for each of ``i0`` - ``i4``
and then store those boxes in instances of ``ResOperation``. The list of such
operations would then go to the optimizer. Those lists are big - we usually
remove ``90%`` of them during optimizations, but they can be couple thousand
elements. Overall allocating those big lists takes a toll on warmup time,
especially due to the GC pressure. The branch removes the existance of ``Box``
completely, instead using link to ``ResOperation`` itself. So say in the above
example, ``i2`` would refer to its producer - ``i2 = int_add(i0, i1)`` with
arguments getting special treatment.

That alone reduces the GC pressure slightly, but a reduced number
of instances also lets us store references on them directly instead
of going through expensive dictionaries, which were used to store optimizing
information about the boxes. Overall
we measured about 50% speed improvement in the optimizer, which reduces
the overall warmup time between 10% and 30%. The very
`obvious warmup benchmark`_ got a speedup from 4.5s to 3.5s so almost
30% improvement. Obviously the speedups on benchmarks would vastly
depend on how much warmup time is there in those benchmarks. We observed
annotation of pypy to decrease by about 30% and the overall translation
time by about 7%, so your mileage may vary.

Of course, as usual with the large refactoring of a crucial piece of PyPy,
there are expected to be bugs. We are going to wait for the default to stabilize
and you should see warmup improvements in the next release. If you're not afraid
to try, `nightlies`_ will already have them.

.. _`obvious warmup benchmark`: https://bitbucket.org/pypy/benchmarks/src/fe2e89c0ae6846e3a8d4142106a4857e95f17da7/warmup/function_call2.py?at=default
.. _`nightlies`: http://buildbot.pypy.org/nightly/trunk

Cheers!
fijal & arigo

