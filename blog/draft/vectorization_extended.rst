We are happy to announce that both the PowerPC backend and the s390x backend
have been enhanced. Both are now capable to emit SIMD instructions vectorized
loops. Special thanks to IBM for funding this work.


If you are not familiar with this topic you can more details here.


There are many more enhancements under the hood. Most notably, all pure
operations are now delayed to the latest possible point. In some cases indices
has been calculated more than once or they needed an additional register,
because the old value is still used. Additionally it is now possible to load
quadword aligned memory in both ppc and s390x (x86 currently cannot do that).

NumPy & CPyExt
--------------

The community and core development effort pushes CPyExt towards a complete, but
emulated layer for CPython C extensions. This is great, because the one
restriction preventing the deployment of PyPy in several scenarios is soon going
to be removed. We advocate not to use the CPyExt, but rather to not write C code
at all (let PyPy speed up your Python code) or use cffi.


The work done in this project helps micro numpy (NumPyPy) to speed up the
operations for ppc and s390x. But, NumPyPy and NumPy ... do we need both? There
are several cases where one of them is not the best performing solution. Our
plans are to integrate both, use one of the solutions where we know the other
one will not perform well.


Just to give you an idea why this is a benefit:


NumPy arrays can carry custom dtypes and apply user defined python functions on
the arrays. How could one optimize this kind of scenario? In traditional setup,
you cannot. But as soon as Micro NumPy is turned on, you can suddenly JIT
compile this code and vectorize it.

Another example is element access that occurs frequently, or any other calls
that cross to the C level more frequently.


Benchmarks
----------

Let's have a look at some benchmarks reusing mikefc's numpy benchmark suite. The
suite only runs a subset of all commands showing that the core functionality is
properly working. Additionally it has been rewritten to use perf instead of the
timeit stdlib module.


Setup
-----
x86 runs on a Intel i7-2600 clocked at 3.40GHz using 4 cores. PowerPC runs on
the Power 8 clocked at 3.425GHz providing 160 cores. Last but not least the
mainframe machine clocked up to 4 GHz, but fully virtualized (as it is common
for such machines).


As you can see all machines run very different configurations. It does not make
sense to compare across platforms, but rather implementations on the same
platform.







Blue shows CPython 2.7.10+ available on that platform using the latest NumPy
(1.11). Micro NumPy is used for PyPy. PyPy+ indicates that the vectorization
optimization is turned on.

All bar charts show the median value of all runs (5 samples, 100 loops, 10 inner
loops, for the operations on vectors (not matrices) the loops are set to 1000).
PyPy additionally gets 3 extra executions to warmup the JIT.


The comparison is really comparing speed of machine code. It compares the PyPy's
JIT output vs GCC's output. It has little to do with the speed of the
interpreter.


Both new SIMD backends speedup the numeric kernels. Some times it is near to the
speed of CPython (note that PyPy will execute the machine code kernel after a
interpreting it at least 1000 times), some times it is faster. The maximum
parallelism very much depends on the extension emitted by the compiler. All
three SIMD backends have the same core register size (which is 128 bit). This
means that all three behave similar but ppc and s390x gain more because they can
load 128bit of memory from quadword aligned memory.


Future directions
-----------------

Python seems to be in an ongoing transition from a language used mostly for web
development to also be used in data science. This is currently starting to
emerge in Europe and Python is already heavily used for data science in the
United States of America and many other places around the world.


I believe that PyPy has a valuable contribution for data scientists, helping
them to rapidly write scientific programs in Python and run them at near native
speed. If you happen to be in that situation, we are eager to hear you feedback
or resolve your issues and also work together to improve your simulations,
calculations, .... Just get in touch!

Richard Plangger (plan_rich) and the PyPy team
