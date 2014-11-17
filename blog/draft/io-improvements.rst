
Hello everyone!

We've wrapped up the Warsaw sprint, so I would like to describe some
branches which have been recently merged and which improved the I/O and the
GC: `gc_no_cleanup_nursery`_ and `gc-incminimark-pinning`_.

.. _`gc_no_cleanup_nursery`: https://bitbucket.org/pypy/pypy/commits/9e2f7a37c1e2
.. _`gc-incminimark-pinning`: https://bitbucket.org/pypy/pypy/commits/64017d818038

The first branch was started by Wenzhu Man for her Google Summer of Code
and finished by Maciej Fijałkowski and Armin Rigo.
The PyPy GC works by allocating new objects in the young object
area (the nursery), simply by incrementing a pointer. After each minor
collection, the nursery has to be cleaned up. For simplicity, the GC used 
to do it by zeroing the whole nursery.

This approach has bad effects on the cache, since you zero a large piece of
memory at once and do unnecessary work for things that don't require zeroing
like large strings. We mitigated the first problem somewhat with incremental
nursery zeroing, but this branch removes the zeroing completely, thus
improving the string handling and recursive code (since jitframes don't
requires zeroed memory either). I measured the effect on two examples: 
a recursive implementation of  `fibonacci`_ and `gcbench`_,
to measure GC performance.

.. _`fibonacci`: https://bitbucket.org/pypy/benchmarks/src/69152c2aee7766051aab15735b0b82a46b82b802/own/fib.py?at=default
.. _`gcbench`: https://bitbucket.org/pypy/benchmarks/src/69152c2aee7766051aab15735b0b82a46b82b802/own/gcbench.py?at=default

The results for fibonacci and gcbench are below (normalized to cpython
2.7). Benchmarks were run 50 times each (note that the big standard
deviation comes mostly from the warmup at the beginning, true figures
are smaller):

+----------------+----- ------------+-------------------------+--------------------+
| benchmark      | CPython          | PyPy 2.4                | PyPy non-zero      |
+----------------+------------------+-------------------------+--------------------+
| fibonacci      | 4.8+-0.15 (1.0x) | 0.59+-0.07 (8.1x)       | 0.45+-0.07 (10.6x) |
+----------------+------------------+-------------------------+--------------------+
| gcbench        | 22+-0.36 (1.0x)  | 1.34+-0.28 (16.4x)      | 1.02+-0.15 (21.6x) |
+----------------+------------------+-------------------------+--------------------+

The second branch was done by Gregor Wegberg for his master thesis and finished
by Maciej Fijałkowski and Armin Rigo. Because of the way it works, the PyPy GC from
time to time moves the objects in memory, meaning that their address can change.
Therefore, if you want to pass pointers to some external C function (for
example, write(2) or read(2)), you need to ensure that the objects they are
pointing to will not be moved by the GC (e.g. when running a different thread).
PyPy up to 2.4 solves the problem by copying the data into or from a non-movable buffer, which
is obviously inefficient.
The branch introduce the concept of "pinning", which allows us to inform the
GC that it is not allowed to move a certain object for a short period of time.
This introduces a bit of extra complexity
in the garbage collector, but improves the I/O performance quite drastically,
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

What we can see is that ``os.read`` and ``os.write`` both improved greatly
and outperforms CPython now for each combination. ``file`` operations are
a little more tricky, and while those branches improved the situation a bit,
the improvement is not as drastic as in ``os`` versions.  It really should not
be the case and it showcases how our ``file`` buffering is inferior to CPython.
We plan on removing our own buffering and using ``FILE*`` in C in the near future,
so we should outperform CPython on those too (since our allocations are cheaper).
If you look carefully in the benchmark, the write function is copied three times.
This hack is intended to avoid JIT overspecializing the assembler code, which happens
because the buffering code was written way before the JIT was done. In fact, our buffering
is hilariously bad, but if stars align correctly it can be JIT-compiled to something
that's not half bad. Try removing the hack and seeing how the performance of the last
benchmark drops :-) Again, this hack should be absolutely unnecessary once we remove
our own buffering, stay tuned for more.

Cheers,
fijal

.. _`this benchmark`: https://bitbucket.org/pypy/benchmarks/src/69152c2aee7766051aab15735b0b82a46b82b802/io/iobasic.py?at=default
