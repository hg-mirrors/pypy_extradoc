Software Transactional Memory with PyPy
---------------------------------------

PyPy is a fast alternative Python implementation.  Software
Transactional Memory is a current academic research topic.  Put the two
together --brew for a couple of years-- and we obtain a version of PyPy
that runs on multiple cores, without the infamous Global Interpreter
Lock (GIL).  It has been freshly released in beta, including integration
with the Just-in-Time compiler.

But its point is not only of being "GIL-less": it can give the illusion
of single-threaded programming.  I will give examples of what I mean
exactly by that.  Starting from the usual multithreaded demos, I will
move to other examples where the actual threads are hidden to the
programmer.  I will explain how we can modify the core of async
libraries (Twisted, Tornado, gevent, ...) to use multiples threads,
without exposing any concurrency issues to the user of the library ---
the existing Twisted/etc. programs still run mostly without change.

I will also give an overview of how things work under the cover: the
10000-feet view is to create internally copies of objects and write
changes into these copies.  This allows the originals to continue being
used by other threads.
