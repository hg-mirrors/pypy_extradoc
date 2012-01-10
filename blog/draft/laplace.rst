NumPyPy progress report - running benchmarks
============================================

Hello.

I'm pleased to inform about progress we made on NumPyPy both in terms of
completeness and performance. This post mostly deals with the performance
side and how far we got by now. **Word of warning:** It's worth noting that
the performance work on the numpy side is not done - we're maybe half way
through and there are trivial and not so trivial optimizations to be performed.
In fact we didn't even start to implement some optimizations like vectorization.

Benchmark
---------

We choose a laplace transform, which is also used on scipy's
`PerformancePython`_ wiki. The problem with the implementation on the
performance python wiki page is that there are two algorithms used which
has different convergence, but also very different performance characteristics
on modern machines. Instead we implemented our own versions in C and a set
of various Python versions using numpy or not. The full source is available
on `fijal's hack`_ repo and the exact revision used is 18502dbbcdb3.

Let me describe various algorithms used. Note that some of them contain
pypy-specific hacks to work around current limitations in the implementation.
Those hacks will go away eventually and the performance should improve and
not decrease. It's worth noting that while numerically the algorithms used
are identical, the exact data layout is not and differs between methods.

**Note on all the benchmarks:** they're all run once, but the performance
is very stable across runs.

So, starting from the C version, it implements dead simple laplace transform
using two loops and a double-reference memory (array of ``int**``). The double
reference does not matter for performance and two algorithms are implemented
in ``inline-laplace.c`` and ``laplace.c``. They're both compiled with
``gcc 4.4.5`` and ``-O3``.

A straightforward version of those in python
is implemented in ``laplace.py`` using respectively ``inline_slow_time_step``
and ``slow_time_step``. ``slow_2_time_step`` does the same thing, except
it copies arrays in-place instead of creating new copies.

+-----------------------+----------------------+--------------------+
| bench                 | number of iterations | time per iteration |
+-----------------------+----------------------+--------------------+
| laplace C             | 219                  | 6.3ms              |
+-----------------------+----------------------+--------------------+
| inline-laplace C      | 278                  | 20ms               |
+-----------------------+----------------------+--------------------+
| slow python           | 219                  | 17ms               |
+-----------------------+----------------------+--------------------+
| slow 2 python         | 219                  | 14ms               |
+-----------------------+----------------------+--------------------+
| inline_slow python    | 278                  | 23.7               |
+-----------------------+----------------------+--------------------+

The important thing to notice here that data dependency in the inline version
is causing a huge slowdown. Note that this is already **not too bad**,
as in yes, the braindead python version of the same algorithm takes longer
and pypy is not able to use as much info about data being independent, but this
is within the same ballpark - **15% - 170%** slower than C, but it definitely
matters more which algorithm you choose than which language. For a comparison,
slow versions take about **5.75s** each on CPython 2.6 **per iteration**,
so estimating, they're about **200x** slower than the PyPy equivalent.
I didn't measure full run though :)

Next step is to use numpy expressions. The first problem we run into is that
computing the error walks again the entire array. This is fairly inefficient
in terms of cache access, so I took a liberty of computing errors every 15
steps. This makes convergence rounded to the nearest 15 iterations, but
speeds things up anyway. ``numeric_time_step`` takes the most braindead
approach of replacing the array with itself, like this::

  u[1:-1, 1:-1] = ((u[0:-2, 1:-1] + u[2:, 1:-1])*dy2 + 
                         (u[1:-1,0:-2] + u[1:-1, 2:])*dx2)*dnr_inv

We need 3 arrays here - one for an intermediate (pypy does not automatically
create intermediates for expressions), one for a copy to compute error and
one for the result. This works a bit by chance, since numpy ``+`` or
``*`` creates an intermediate and pypy simulates the behavior if necessary.

``numeric_2_time_step`` works pretty much the same::

  src = self.u
  self.u = src.copy()
  self.u[1:-1, 1:-1] = ((src[0:-2, 1:-1] + src[2:, 1:-1])*dy2 + 
                        (src[1:-1,0:-2] + src[1:-1, 2:])*dx2)*dnr_inv

except the copy is now explicit rather than implicit.

``numeric_3_time_step`` does the same thing, but notices you don't have to copy
the entire array, it's enough to copy border pieces and fill rest with zeros::

        src = self.u
        self.u = numpy.zeros((self.nx, self.ny), 'd')
        self.u[0] = src[0]
        self.u[-1] = src[-1]
        self.u[:, 0] = src[:, 0]
        self.u[:, -1] = src[:, -1]
        self.u[1:-1, 1:-1] = ((src[0:-2, 1:-1] + src[2:, 1:-1])*dy2 + 
                              (src[1:-1,0:-2] + src[1:-1, 2:])*dx2)*dnr_inv

``numeric_4_time_step`` is the one that tries to resemble the C version more.
Instead of doing an array copy, it actually notices that you can alternate
between two arrays. This is exactly what C version does.
Note the ``remove_invalidates`` call that's a pypy specific hack - we hope
to remove this call in the near future, but in short it promises "I don't
have any unbuilt intermediates that depend on the value of the argument",
which means you don't have to compute expressions you're not actually using::

        remove_invalidates(self.old_u)
        remove_invalidates(self.u)
        self.old_u[:,:] = self.u
        src = self.old_u
        self.u[1:-1, 1:-1] = ((src[0:-2, 1:-1] + src[2:, 1:-1])*dy2 + 
                              (src[1:-1,0:-2] + src[1:-1, 2:])*dx2)*dnr_inv

This one is the most equivalent to the C version.

``numeric_5_time_step`` does the same thing, but notices you don't have to
copy the entire array, it's enough to just copy edges. This is an optimization
that was not done in the C version::

        remove_invalidates(self.old_u)
        remove_invalidates(self.u)
        src = self.u
        self.old_u, self.u = self.u, self.old_u
        self.u[0] = src[0]
        self.u[-1] = src[-1]
        self.u[:, 0] = src[:, 0]
        self.u[:, -1] = src[:, -1]
        self.u[1:-1, 1:-1] = ((src[0:-2, 1:-1] + src[2:, 1:-1])*dy2 + 
                              (src[1:-1,0:-2] + src[1:-1, 2:])*dx2)*dnr_inv

Let's look at the table of runs. As above, ``gcc 4.4.5``, compiled with
``-O3``, pypy nightly 7bb8b38d8563, 64bit platform. All of the numeric methods
run 226 steps each, slightly more than 219, rounding to the next 15 when
the error is computed. Comparison for PyPy and CPython:

+-----------------------+-------------+----------------+
| benchmark             | PyPy        | CPython        |
+-----------------------+-------------+----------------+
| numeric               | 21ms        | 35ms           |
+-----------------------+-------------+----------------+
| numeric 2             | 14ms        | 37ms           |
+-----------------------+-------------+----------------+
| numeric 3             | 13ms        | 29ms           |
+-----------------------+-------------+----------------+
| numeric 4             | 11ms        | 31ms           |
+-----------------------+-------------+----------------+
| numeric 5             | 9.3ms       | 21ms           |
+-----------------------+-------------+----------------+

So, I can say that those preliminary results are pretty ok. They're not as
fast as the C version, but we're already much faster than CPython, almost
always more than 2x on this relatively real-world example. This is not the
end though. As we continue work, we hope to use a much better high level
information that we have about operations to eventually outperform C, hopefully
in 2012. Stay tuned.

Cheers,
fijal

.. _`PerformancePython`: http://www.scipy.org/PerformancePython
