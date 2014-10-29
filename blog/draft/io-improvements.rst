
Hello everyone!

We're about to wrap up the Warsaw sprint, so I would like to describe some
branches we merged before or during the sprint. This blog post describes
two branches, one with IO improvements the other one with GC improvements.

The first one was a branch started by Wenzhu Man during the summer of code
and finished by Maciej Fijalkowski and Armin Rigo about not zeroing the nursery.
The way PyPy GC works is that it allocates new objects in the young object
area (the nursery) using bump pointer generation. To simplify things we
used to zero the nursery beforehand, because all the GC references can't
point to random memory. This both affects cache, since you zero a large
memory at once and does unnecessary work for things that don't require zeroing
like large strings. We somehow mitigated the first problem with incremental
nursery zeroing, but this branch removes the zeroing completely, thus
improving the string handling and recursive code (since jitframes don't
requires zeroed memory either). I run the effect on three examples, one
`doing IO`_ in a loop, second one running famous `fibonacci`_ recursively,
which I would argue is a good fit this one time and the last one running
`gcbench`_. The results for fibonacci and gcbench are below
(normalized to cpython 2.7). Benchmarks were run 50 times each:

XXXX

The second branch was done by Gregor Wegberg for his master thesis and finished
by Maciej Fijalkowski and Armin Rigo. Since in PyPy objects can move in memory,
PyPy 2.4 solves the problem by copying a buffer before calling read or write.
This is obviously inefficient. The branch "pins" the objects for a short period
of time, by making sure they can't move. This introduces slight complexity
in the garbage collector, where bump pointer allocator needs to "jump over"
pinned objects, but improves the IO quite drastically. In this benchmark
we either write a number of bytes from a freshly allocated string into
/dev/null or read a number of bytes from /dev/full. I'm showing the results
for PyPy 2.4, PyPy with non-zero-nursery and PyPy with non-zero-nursery and
object pinning. Those are wall times for cases using ``os.read/os.write``
and ``file.read/file.write``, normalized against CPython 2.7.

Benchmarks were done using PyPy 2.4 and revisions ``85646d1d07fb`` for
non-zero-nursery and ``3d8fe96dc4d9`` for non-zero-nursery and pinning.
The benchmarks were run once, since the standard deviation was small.

XXXX

XXX summary
