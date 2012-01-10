NumPyPy progress report - running benchmarks
============================================

Hello.

I'm pleased to inform you about the progress we have made on NumPyPy, both in
terms of completeness and performance. This post mostly deals with the
performance side and how far we have come so far. **Word of warning:** the
performance work on NumPyPy isn't done - we're maybe half way to where we want
to be and there are many trivial and not so trivial optimizations to be
performed. In fact we haven't even started to implement important
optimizations, like vectorization.

Benchmark
---------

We choose a laplace transform, based on SciPy's `PerformancePython`_ wiki.
Unfortunately, the different implementations on the wiki page accidentally use
two different algorithms, which have different convergences, and very different
performance characteristics on modern computers. As a result, we implemented
our own versions in C and Python (both with and without NumPy). The full source
can be found in `fijal's hack`_ repo, all these benchmarks were performed at
revision 18502dbbcdb3.

First, let me describe various algorithms used. Note that some of them contain
PyPy-specific hacks to work around limitations in the current implementation.
These hacks will go away eventually and the performance should improve. It's
worth noting that while numerically the algorithms used are identical, the
exact data layout in memory differs between them.

**Note on all the benchmarks:** they were all run once, but the performance is
very stable across runs.

Starting with the C version, it implements a dead simple laplace transform
using two loops and a double-reference memory (array of ``int*``). The double
reference does not matter for performance and two algorithms are implemented in
``inline-laplace.c`` and ``laplace.c``. They're both compiled with
``gcc 4.4.5`` at ``-O3``.

A straightforward version of those in Python is implemented in ``laplace.py``
using respectively ``inline_slow_time_step`` and ``slow_time_step``.
``slow_2_time_step`` does the same thing, except it copies arrays in-place
instead of creating new copies.

(XXX: these are timed under PyPy?)

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

An important thing to notice here is that the data dependency in the inline
version causes a huge slowdown for the C versions. This is already not too bad
for us, the braindead Python version takes longer and PyPy is not able to take
advantage of the knowledge that the data is independent, but it is in the same
ballpark - **15% - 170%** slower than C, but the algorithm you choose matters
more than the language. By comparison, the slow versions take about **5.75s**
each on CPython 2.6 **per iteration**, and by estimating, are about **200x**
slower than the PyPy equivalent. I didn't measure the full run though :)

The next step is to use NumPy expressions. The first problem we run into is
that computing the error requires walking the entire array a second time. This
is fairly inefficient in terms of cache access, so I took the liberty of
computing the errors every 15 steps. This results in the convergence being
rounded to the nearest 15 iterations, but speeds things up considerably (XXX:
is this true?). ``numeric_time_step`` takes the most braindead approach of
replacing the array with itself, like this::

  u[1:-1, 1:-1] = ((u[0:-2, 1:-1] + u[2:, 1:-1])*dy2 +
                         (u[1:-1,0:-2] + u[1:-1, 2:])*dx2)*dnr_inv

We need 3 arrays here - one is an intermediate (PyPy does not automatically
create intermediates for expressions), one is a copy for computing the error,
and one is the result. This works by chance, since in NumPy ``+`` or ``*``
creates an intermediate, while NumPyPy avoids allocating the intermediate if
possible.

``numeric_2_time_step`` works pretty much the same::

  src = self.u
  self.u = src.copy()
  self.u[1:-1, 1:-1] = ((src[0:-2, 1:-1] + src[2:, 1:-1])*dy2 +
                        (src[1:-1,0:-2] + src[1:-1, 2:])*dx2)*dnr_inv

except the copy is now explicit rather than implicit.

``numeric_3_time_step`` does the same thing, but notices you don't have to copy
the entire array, it's enough to copy the border pieces and fill rest with
zeros::

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
between two arrays. This is exactly what C version does. The
``remove_invalidates`` call is a PyPy specific hack - we hope to remove this
call in the near future, but in short it promises "I don't have any unbuilt
intermediates that depend on the value of the argument", which means you don't
have to compute sub-expressions you're not actually using::

        remove_invalidates(self.old_u)
        remove_invalidates(self.u)
        self.old_u[:,:] = self.u
        src = self.old_u
        self.u[1:-1, 1:-1] = ((src[0:-2, 1:-1] + src[2:, 1:-1])*dy2 +
                              (src[1:-1,0:-2] + src[1:-1, 2:])*dx2)*dnr_inv

This one is the most equivalent to the C version.

``numeric_5_time_step`` does the same thing, but notices you don't have to copy
the entire array, it's enough to just copy edges. This is an optimization that
was not done in the C version::

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

Let's look at the table of runs. As before, ``gcc 4.4.5``, compiled at ``-O3``,
and PyPy nightly 7bb8b38d8563, on an x86-64 machine. All of the numeric methods
run 226 steps each, slightly more than 219, rounding to the next 15 when the
error is computed. Comparison for PyPy and CPython:

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
+-----------------------+-------------+-----------------

We think that these preliminary results are pretty good, they're not as fast as
the C version (or as fast as we'd like them to be), but we're already much
faster than NumPy on CPython, almost always by more than 2x on this relatively
real-world example. This is not the end though, in fact it's hardly the
beginning: as we continue work, we hope to make even much better use of the
high level information that we have, in order to eventually outperform C,
hopefully in 2012. Stay tuned.

Cheers,
fijal

.. _`PerformancePython`: http://www.scipy.org/PerformancePython
