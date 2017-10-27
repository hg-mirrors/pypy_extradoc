We are happy to announce that JIT support in both the PowerPC backend and the
s390x backend have been enhanced. Both can now vectorize loops via SIMD
instructions. Special thanks to IBM for funding this work.


If you are not familiar with this topic you can more details here_.


There are many more enhancements under the hood. Most notably, all pure
operations are now delayed until the latest possible point. In some cases indices
have been calculated more than once or they needed an additional register,
because the old value is still used. Additionally it is now possible to load
quadword-aligned memory in both PPC and s390x (x86 currently cannot do that).


.. _here: http://pypyvecopt.blogspot.co.at

NumPy & CPyExt
--------------

The community and core developers have been moving CPyExt towards a complete, but
emulated, layer for CPython C extensions. This is great, because the one
restriction preventing the wider deployment of PyPy in several scenarios will
hopefully 
be removed. However, we advocate not to use CPyExt, but rather to not write C code
at all (let PyPy speed up your Python code) or use cffi_.


The work done here to support vectorization helps ``micronumpy`` (NumPyPy) to speed up 
operations for PPC and s390x. So why is PyPy supporting both NumPyPy and NumPy, do we 
actually need both? Yes, there are places where gcc can beat the JIT, and places
where the tight integration between NumPyPy and  PyPy is more performant We do
have
plans to integrate both, hijacking the C-extension method calls to use NumPyPy where we 
know NumPyPy can be faster.


Just to give you an idea why this is a benefit:


NumPy arrays can carry custom dtypes and apply user defined python functions on
the arrays. How could one optimize this kind of scenario? In traditional setup,
you cannot. But as soon as NumPyPy is turned on, you can suddenly JIT
compile this code and vectorize it.

Another example is element access that occurs frequently, or any other calls
that cross between Python and the C level frequently.

.. _cffi: http://cffi.readthedocs.io/en/latest

Benchmarks
----------

Let's have a look at some benchmarks reusing `mikefc's numpy benchmark suite`_.
I only ran a subset of microbenchmarks, showing that the core functionality is
functioning properly. Additionally I use ``perf`` instead of the ``timeit`` stdlib module.

.. _`mikefc's numpy benchmark suite`: https://bitbucket.org/mikefc/numpy-benchmark

Setup
-----
x86 runs on a Intel i7-2600 clocked at 3.40GHz using 4 cores. PowerPC runs on
the Power 8 clocked at 3.425GHz providing 160 cores. Last but not least the
mainframe machine ran clocked up to 4 GHz, but fully virtualized (as it is common
for such machines).


As you can see all machines run very different configurations. It does not make
sense to compare across platforms, but rather implementations on the same
platform.







Blue shows CPython 2.7.10+ available on that platform using the latest NumPy
(1.11). NumPyPy is used for PyPy. PyPy+ indicates that the vectorization
optimization is turned on.

All bar charts show the median value of all runs (5 samples, 100 loops, 10 inner
loops, for the operations on vectors (not matrices) the loops are set to 1000).
PyPy additionally gets 3 extra executions to warmup the JIT.


The comparison is really comparing speed of machine code. It compares the PyPy's
JIT output vs GCC's output. These microbenchmarks have little to do with the speed of the
interpreter.


Both new SIMD backends speedup the numeric kernels. Sometime it is near to the
speed of CPython (note that PyPy will execute the machine code kernel after a
interpreting it at least 1000 times), sometime it is faster. The maximum
parallelism very much depends on the extension emitted by the compiler. All
three SIMD backends have the same core register size (which is 128 bit). This
means that all three behave similar but ppc and s390x gain more because they can
load 128bit of memory from quadword aligned memory.


Future directions
-----------------

Python is achieving rapid adoption in data science. This is currently a trend
emerge in Europe, and Python is already heavily used for data science in the
USA many other places around the world.


I believe that PyPy can make a valuable contribution to data scientists, helping
them to rapidly write scientific programs in Python and run them at near native
speed. If you happen to be in that situation, we are eager to hear you feedback
or resolve your issues and also work together to improve the performance of your,
code. Just get in touch!

Richard Plangger (plan_rich) and the PyPy team
