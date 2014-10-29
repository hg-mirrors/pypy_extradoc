
Hello everyone!

We're about to wrap up the Warsaw sprint, so I would like to describe some
branches which have been recently merged and which improved the I/O and the
GC: `gc_no_cleanup_nursery`_ and `gc-incminimark-pinning`_.

The first branch was started by Wenzhu Man for her Google Summer of Code
and finished by Maciej Fijalkowski and Armin Rigo.
The PyPy GC works by allocating new objects in the young object
area (the nursery), simply by incrementing a pointer. After each minor
collection, the nursery has to be cleaned up. For simplicity, the GC used 
to do it by zeroing the whole nursery.

This approach has bad effects on cache, since you zero a large
memory at once and does unnecessary work for things that don't require zeroing
like large strings. We somehow mitigated the first problem with incremental
nursery zeroing, but this branch removes the zeroing completely, thus
improving the string handling and recursive code (since jitframes don't
requires zeroed memory either). I measured the effect on two examples: 
a recursive implementation of  `fibonacci`_ and `gcbench`_,
to measure GC performance.

The results for fibonacci and gcbench are below (normalized to cpython
2.7). Benchmarks were run 50 times each:

XXXX

The second branch was done by Gregor Wegberg for his master thesis and finished
by Maciej Fijalkowski and Armin Rigo. Because of the way it works, the PyPy GC from
time to time moves the objects in memory, meaning that their address can change.
Therefore, if you want to pass pointers to some external C function (for
example, write(2) or read(2)), you need to ensure that the objects they are
pointing to will not be moved by the GC.
PyPy 2.4 solves the problem by copying the data into a non-movable buffer, which
is obviously inefficient.
The branch introduce the concept of "pinning", which allows us to inform the
GC that it is not allowed to move a certain object for a short period of time.
This introduces a bit of extra complexity
in the garbage collector, but improves the the I/O performance quite drastically,
because we no longer need the extra copy to and from the non-movable buffers.

In `this benchmark`_, which does I/O in a loop,
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
