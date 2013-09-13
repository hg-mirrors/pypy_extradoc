Software Transactional Memory with PyPy
---------------------------------------

PyPy is a fast alternative Python implementation.  Software
Transactional Memory is a current academic research topic.  Put the two
together --brew for a couple of years-- and we get a version of PyPy
that runs on multiple cores, without the infamous Global Interpreter
Lock (GIL).  It has been freshly released in beta, including integration
with the Just-in-Time compiler.

But its point is not only of being "GIL-less": it can also give the illusion
of single-threaded programming.  I will give examples of what exactly I mean
by that.  Starting from the usual explicitly multithreaded demos, I will
move to other examples where the actual threads are hidden from the
programmer.  I will explain how the core of async
libraries (Twisted, Tornado, gevent, ...) can be modified to use multiples threads,
without exposing any concurrency issues to the user of the library ---
existing Twisted/etc. programs still run correctly without change.
(They may need a few small changes to enable parallelism.)

I will also give an overview of how things work under the cover: the
10000-feet view is to internally create copies of objects and write
changes into these copies.  This allows the originals to continue being
used by other threads.
