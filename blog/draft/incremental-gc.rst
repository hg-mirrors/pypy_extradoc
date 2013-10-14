Incremental Garbage Collector in PyPy
=====================================

Hello everyone.

We're pleased to announce that as of today (so tomorrow's nightly),
the default PyPy comes with a GC that has much smaller pauses than yesterday.

Let's start with explaining roughly what GC pauses are. In CPython each
object has a reference count, which is incremented each time we create
references and decremented each time we forget them. This means that objects
are freed each time they become unreachable. That is only half of the story
though. Consider code like this::

   class A(object):
        pass

   a = A()
   b = A()
   a.item = b
   b.item = a
   del a
   del b

This creates a reference cycle. It means that while we deleted references to
``a`` and ``b`` from the current scope, they still have a reference count of 1,
because they point to each other, even though the whole group has no references
from the outside. CPython employs a cyclic garbage collector which is used to
find such cycles. It walks over all objects in memory, starting from some known
roots, such as ``type`` objects, variables on the stack, etc. This solves the
problem, but can create noticable GC pauses as the heap becomes large and
convoluted.

PyPy essentially has only the cycle finder - it does not bother with reference
counting, instead it walks alive objects every now and then (this is a big
simplification, PyPy's GC is much more complex than this). As a result it also
has the problem of GC pauses. To alleviate this problem, which is essential for
applications like games, we started to work on incremental GC, which spreads
the walking of objects and cleaning them across the execution time in smaller
intervals. The work was sponsored by the Raspberry Pi foundation, started
by Andrew Chambers and finished by Armin Rigo and Maciej Fijałkowski.

Benchmarks
==========



Nitty gritty details
====================


