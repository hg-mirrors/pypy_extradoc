Update on STM
=============

Hi all,

the sprint in London was a lot of fun and very fruitful. In the last
update on STM, Armin was working on improving and specializing the 
automatic barrier placement.
There is still a lot to do in that area, but that work was merged and
lowered the overhead of STM over non-STM to around **XXX**. The same
improvement has still to be done in the JIT.

But that is not all. Right after the sprint, we were able to squeeze
the last obvious bugs in the STM-JIT combination. However, the performance
was nowhere near to what we want. So until now, we fixed some of the most
obvious issues. Many come from RPython erring on the side of caution
and e.g. making a transaction inevitable even if that is not strictly
necessary, thereby limiting parallelism.
**XXX any interesting details? transaction breaks maybe? guard counters?**
There are still many performance issues of various complexity left
to tackle. So stay tuned or contribute :)

Now, since the JIT is all about performance, we want to at least 
show you some numbers that are indicative of things to come.
Our set of STM benchmarks is very small unfortunately 
(something you can help us out with), so this is 
not representative of real-world performance. We tried to
minimize the effect of JIT warm-up in the benchmark results.


**Raytracer** from `stm-benchmarks <https://bitbucket.org/Raemi/stm-benchmarks/src>`_:
Render times in seconds for a 1024x1024 image:

+-------------+----------------------+-------------------+
| Interpreter | Base time: 1 thread  | 8 threads         |
+=============+======================+===================+
| PyPy-2.1    |    2.47              |     2.56          |
+-------------+----------------------+-------------------+
| CPython     |    81.1              |     73.4          |
+-------------+----------------------+-------------------+
| PyPy-STM    |    50.2              |     10.8          |
+-------------+----------------------+-------------------+

For comparison, disabling the JIT gives 148ms on PyPy-2.1 and 87ms on
PyPy-STM (with 8 threads).

**Richards** from `PyPy repository on the stmgc-c4
branch <https://bitbucket.org/pypy/pypy/commits/branch/stmgc-c4>`_:
Average time per iteration in milliseconds using 8 threads:

+-------------+----------------------+-------------------+
| Interpreter | Base time: 1 thread  | 8 threads         |
+=============+======================+===================+
| PyPy-2.1    |   15.6               |  15.4             |
+-------------+----------------------+-------------------+
| CPython     |   239                |  237              |
+-------------+----------------------+-------------------+
| PyPy-STM    |   371                |  116              |
+-------------+----------------------+-------------------+

For comparison, disabling the JIT gives 492ms on PyPy-2.1 and 538ms on
PyPy-STM.

All this can be found in the `PyPy repository on the stmgc-c4
branch <https://bitbucket.org/pypy/pypy/commits/branch/stmgc-c4>`_.
Try it for yourself, but keep in mind that this is still experimental
with a lot of things yet to come.

You can also download a prebuilt binary from here: **XXX**

As a summary, what the numbers tell us is that PyPy-STM is, as expected,
the only of the three interpreters where multithreading gives a large
improvement in speed.  What they also tell us is that, obviously, the
result is not good enough *yet:* it still takes longer on a 8-threaded
PyPy-STM than on a regular single-threaded PyPy-2.1.  As you should know
by now, we are good at promizing speed and delivering it years later.
It has been two years already since PyPy-STM started, so we're in the
fast-progressing step right now :-)
