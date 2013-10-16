Update on STM
=============

Hi all,

The sprint in London was a lot of fun and very fruitful. In the last
update on STM, Armin was working on improving and specializing the 
automatic barrier placement. There is still a lot to do in that area, 
but that work is merged now. Specializing and improving barrier placement
is still to be done for the JIT.

But that is not all. Right after the sprint, we were able to squeeze
the last obvious bugs in the STM-JIT combination. However, the performance
was nowhere near to what we want. So until now, we fixed some of the most
obvious issues. Many come from RPython erring on the side of caution
and e.g. making a transaction inevitable even if that is not strictly
necessary, thereby limiting parallelism. Another problem came from 
increasing counters everytime a guard fails, which caused transactions
to conflict on these counter updates. Since these counters do not have
to be completely accurate, we update them non-transactionally now with
a chance of small errors.

There are still many such performance issues of various complexity left
to tackle: we are nowhere near done. So stay tuned or contribute :)

Performance
-----------

Now, since the JIT is all about performance, we want to at least 
show you some numbers that are indicative of things to come.
Our set of STM benchmarks is very small unfortunately 
(something you can help us out with), so this is 
not representative of real-world performance. We tried to
minimize the effect of JIT warm-up in the benchmark results.

The machine these benchmarks were executed on has 4 physical
cores with Hyper-Threading (8 hardware threads).


**Raytracer** from `stm-benchmarks <https://bitbucket.org/Raemi/stm-benchmarks/src>`_:
Render times in seconds for a 1024x1024 image:

+-------------+----------------------+---------------------+
| Interpreter | Base time: 1 thread  | 8 threads (speedup) |
+=============+======================+=====================+
| PyPy-2.1    |    2.47              |     2.56 (0.96x)    |
+-------------+----------------------+---------------------+
| CPython     |    81.1              |     73.4 (1.1x)     |
+-------------+----------------------+---------------------+
| PyPy-STM    |    50.2              |     10.8 (4.6x)     |
+-------------+----------------------+---------------------+

For comparison, disabling the JIT gives 148s on PyPy-2.1 and 87s on
PyPy-STM (with 8 threads).

**Richards** from `PyPy repository on the stmgc-c4
branch <https://bitbucket.org/pypy/pypy/commits/branch/stmgc-c4>`_:
Average time per iteration in milliseconds:

+-------------+----------------------+---------------------+
| Interpreter | Base time: 1 thread  | 8 threads (speedup) |
+=============+======================+=====================+
| PyPy-2.1    |   15.6               |  15.4 (1.01x)       |
+-------------+----------------------+---------------------+
| CPython     |   239                |  237 (1.01x)        |
+-------------+----------------------+---------------------+
| PyPy-STM    |   371                |  116 (3.2x)         |
+-------------+----------------------+---------------------+

For comparison, disabling the JIT gives 492ms on PyPy-2.1 and 538ms on
PyPy-STM.

Try it!
-------

All this can be found in the `PyPy repository on the stmgc-c4
branch <https://bitbucket.org/pypy/pypy/commits/branch/stmgc-c4>`_.
Try it for yourself, but keep in mind that this is still experimental
with a lot of things yet to come. Only Linux x64 is supported right
now, but contributions are welcome.

You can download a prebuilt binary from here:
https://bitbucket.org/pypy/pypy/downloads/pypy-oct13-stm.tar.bz2
(Linux x64 Ubuntu >= 12.04).

Summary
-------

What the numbers tell us is that PyPy-STM is, as expected,
the only of the three interpreters where multithreading gives a large
improvement in speed.  What they also tell us is that, obviously, the
result is not good enough *yet:* it still takes longer on a 8-threaded
PyPy-STM than on a regular single-threaded PyPy-2.1.  However, as you
should know by now, we are good at promising speed and delivering it...
years later ``:-)``  But it has been two years already since PyPy-STM
started, and things look good now.  Expect major improvements soon.


Cheers

Armin & Remi
