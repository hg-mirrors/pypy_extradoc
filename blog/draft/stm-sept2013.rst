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
was nowhere near what we want. So until now, we fixed some of the most
obvious issues. Many come from RPython erring on the side of caution
and e.g. making a transaction inevitable even if that is not strictly
necessary, thereby limiting parallelism.
**XXX any interesting details?**
There are still many performance issues of various complexity left
to tackle. So stay tuned or contribute :)

Now, since the JIT is all about performance, we want to at least 
show you some numbers that are indicative of things to come.
Our set of STM benchmarks is very small unfortunately 
(something you can help us out with), so this is 
not representative of real-world performance.

**Raytracer** from `stm-benchmarks <https://bitbucket.org/Raemi/stm-benchmarks/src>`_:
Render times for a 1024x1024 image using 6 threads

+-------------+----------------------+
| Interpeter  | Time (no-JIT / JIT)  |
+=============+======================+
| PyPy-2.1    | ... / ...            |
+-------------+----------------------+
| CPython     | ... / -              |
+-------------+----------------------+
| PyPy-STM    | ... / ...            |
+-------------+----------------------+

**XXX same for Richards**


All this can be found in the `PyPy repository on the stmgc-c4
branch <https://bitbucket.org/pypy/pypy/commits/branch/stmgc-c4>`_.
Try it for yourself, but keep in mind that this is still experimental
with a lot of things yet to come.

You can also download a prebuilt binary frome here: **XXX**


