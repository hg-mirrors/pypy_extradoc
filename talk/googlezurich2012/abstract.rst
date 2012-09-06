
PyPy
============================================================

The PyPy project has recently gathered a lot of attention for its
progress in speeding up the Python language -- it is the fastest,
most compatible and most stable 'alternative´ Python interpreter.  No
longer merely a research curiosity, PyPy is now suitable for production
use.

The speed comes from a custom Just-in-Time compiler (JIT).  It is the
first Virtual Machine to have a JIT generated automatically from the
interpreter of the language, which makes it correct and complete by
construction.  The JIT itself is a tracing JIT, roughly similar to
SpiderMonkey.

* most Python benchmarks run much faster than with CPython or Psyco
* the real-world PyPy compiler toolchain itself (200 KLocs) runs twice as fast
* supports x86 (32 or 64 bit), ARM (v7), and soon POWER64
* full compatibility with CPython (more than Jython/IronPython)
* ctypes, CFFI and C++ support to call C/C++ libraries from Python (fast)
* supports Stackless Python (in-progress)
* integrates existing CPython C extensions (slowly)

In this talk we will see examples of what PyPy is best at (pure Python
code that runs for a while), what compatibility issues you may run into
(very few), how to use CPython C extension modules (you can more or
less, but it's slow), as well as dig a bit below the surface and use
some tools to view the x86 machine code that was produced by the JIT.

I will end the talk with an overview of Software Transactional Memory
(STM) and how it promizes to give a PyPy without the Global Interpreter
Lock (GIL), i.e. able to run a single process using multiple cores.
