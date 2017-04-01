We are happy to announce a new release for the PyPI package vmprof.

It is now able to capture native stack frames on Linux and Mac OS X to show you bottle necks in compiled code (such as CFFI modules, Cython or C Python extensions). It supports PyPy, CPython versions 2.7, 3.4, 3.5 and 3.6. Special thanks to Jetbrains for funding the native profiling support.

What is vmprof?
===============

If you have already worked with vmprof you can skip the next two section. If not, here is a short introduction:


The goal of vmprof package is to give you more insight into your program. It is a statistical profiler. Another prominent profiler you might already have worked with is cProfile. It is bundled with the Python standard library.


vmprof's distinct feature (from most other profilers) is that it does not significantly slow down your program execution. The employed strategy is statistical, rather than deterministic. Not every function call is intercepted, but it samples stack traces and memory usage at a configured sample rate (usually around 100hz). You can imagine that this creates a lot less contention than doing work before and after each function call.


As mentioned earlier cProfile gives you a complete profile, but it needs to intercept every function call (it is a deterministic profiler). Usually this means that you have to capture and record every function call, but this takes an significant amount time.


The overhead vmprof consumes is roughly 3-4% of your total program runtime or even less if you reduce the sampling frequency. Indeed it lets you sample and inspect much larger programs. If you failed to profile a large application with cProfile, please give vmprof a shot.


vmprof.com or PyCharm
======================


There are two major alternative to the command line tools shipped with vmprof.

    A web service on vmprof.com
    A commercial version of PyCharm

Since the PyPy Team runs and maintains the service on vmprof.com I'll explain some more details here. Still PyCharm is a great IDE and uses vmprof to display the statistical profiles. We highly recommend to use either of those, the command line tool is only good for quick inspection.


On vmprof.com you can inspect the generated profile interactively instead of looking at console output. What is sent to vmprof.com? You can find details here.


There are currently three visualizations we'll quickly explain:


Flamegraph: Accumulates and displays the most frequent codepaths. It allows you to quickly and accurately identify hot spots in your code. The flame graph below is a very short run of richards.py (less. Thus it shows a lot of time spent in PyPy's JIT compiler.

<image>

List all functions (optionally sorted): the equivalent of the vmprof command line output in the web.

<image>

Memory curve: A line plot that shows how how many MBytes have been consumed over the lifetime of your program (see more info in the section below).

<image>

Native programs
===============

The new feature introduced in vmprof 0.4.0 allows you to look beyond the Python level. As you might know, Python maintains a stack of frames to save the execution. Up to now the vmprof profiles only contained that level of information. But what if you program jumps to native code (such as calling gzip compression on a large file)? Up to now you would not see that information.


Many packages make use of the CPython C API (which we discurage, please lookup cffi for a better way to call C). Have you ever had the issue that you know that your performance problems reach down to, but you could not profile it properly? Now you can!


Let's inspect a very simple Python program to find out why a program is significantly slower on Linux than on Mac:


import numpy as np
n = 1000
a = np.random.random((n, n))
b = np.random.random((n, n))
c = np.dot(np.abs(a), b)


Take two NxN random matrix objects and create a dot product. The first argument to the dot product provides the absolute value of the random matrix.


Run, Python, NumPy, OS, n=..., Took
[1] CPython 3.5.2, NumPy 1.12.1, Mac OS X, 10.12.3, n=5000, ~9 sec
[2] CPython 3.6.0, NumPy 1.12.1, Linux 64, Kernel 4.9.14, n=1000, ~26 sec

Note that the Linux machine operates on a 5 times smaller matrix, still it takes much longer. What is wrong? Is Linux slow? CPython 3.6.0? Well no, lets inspect and [1] and [2] (shown below in that order).

[2] runs on Linux, spends nearly all of the time in PyArray_MatrixProduct2, if you compare to [1] on Mac OS X, you'll see that a lot of time is spent in generating the random numbers and the rest in cblas_matrixproduct.

Blas has a very efficient implementation so you can achieve the same on Linux if you install a blas implementation (such as openblas).

Usually you can spot potential program source locations that take a lot of time and might be the first starting point to resolve performance issues.

Beyond Python programs
======================


It is not unthinkable that the strategy can be reused for native programs. Indeed this can already be done by creating a small cffi wrapper around an entry point of a compiled C program. It would even work for programs compiled from other languages (e.g. C++ or Fortran). The resulting function names are the full symbol name embedded into either the executable symboltable or extracted from the dwarf debugging information. Most of those will be compiler specific and contain some cryptic information.

Memory profiling
================

We thankfully received a code contribution from the company Blue Yonder. They have built a memory profiler (for Linux and Mac OS X) on top of vmprof.com that displays the memory consumption for the runtime of your process.

You can run it the following way:


$ python -m vmprof --mem --web script.py


By adding --mem, vmprof will capture memory information and display it in the dedicated view on vmprof.com. You can tha view by by clicking the 'Memory' switch in the flamegraph view.


There is more


Some more minor highlights contained in 0.4.x:

    VMProf support for Windows 64 bit (python only)
    VMProf can read profiles generated by another host system
    VMProf is now bundled in several binary wheel for fast and easy installation (Mac OS X, Linux 32/64 for CPython 2.7, 3.4, 3.5, 3.6)

Future plans - Profile Streaming
================================


vmprof has not reached the end of development. There are many features we could implement. But there is one feature that could be a great asset to many Python developers.


Continuous delivery of your statistical profile, or in short, profile streaming. One of the great strengths of vmprof is that is consumes very little overhead. It is not a crazy idea to run this in production.


It would require a smart way to stream the profile in the background to vmprof.com and new visualizations to look at much more data your Python service produces.


If that sounds like a solid vmprof improvement, don't hesitate to get in touch with us (e.g. IRC #pypy, mailing list pypy-dev, or comment below)


You can help!
=============


There are some immediate things other people could help with. Either by donating time or money (yes we have occasional contributors which is great)!

    We gladly received code contribution for the memory profiler. But it was not enough time to finish the migration completely. Sadly it is a bit brittle right now.
    We would like to spend more time on other visualizations. This should include to give a much better user experience on vmprof.com (like a tutorial that explains the visualization that we already have). 
    Build Windows 32/64 bit wheels (for all CPython versions we currently support)

We are also happy to accept google summer of code projects on vmprof for new visualizations and other improvements. If you qualify and are interested, don't hesitate to ask!


Richard Plangger (plan_rich) and the PyPy Team


[1] Mac OS X http://vmprof.com/#/567aa150-5927-4867-b22d-dbb67ac824ac
[2] Linux64 http://vmprof.com/#/097fded2-b350-4d68-ae93-7956cd10150c
