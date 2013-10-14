Incremental Garbage Collector in PyPy
=====================================

Hello everyone.

We're pleased to announce that as of today (so tomorrow's nightly),
the default PyPy comes with a GC that has much smaller pauses than yesterday.

Let's start with explaining roughly what GC pauses are. In CPython each
object has a reference count, which is incremented each time we create
references and decremented each time we forget them. This means that objects
(XXX also, very long chains of objects cause unbounded pauses in CPython)
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

This was done as a patch to "minimark", our current GC, and called
"incminimark" for now.  The former is a generational stop-the-world GC.
New objects are allocated "young", i.e. in the nursery, a special zone
of a few MB of memory.  When it is full, a "minor collection" step moves
the surviving objects out of the nursery.  This can be done quickly (a
few millisecond at most) because we only need to walk through the young
objects that survive --- usually a small fraction of all young objects.
From time to time, this minor collection is followed by a "major
collection": in that step, we walk *all* objects to classify which ones
are still alive and which ones are now dead (*marking*) and free the
memory occupied by the dead ones (*speeding*).

This "major collection" is what gives the long GC pauses.  To fix this
problem we made the GC incremental: instead of running one complete
major collection, we split its work into a variable number of pieces
and run each piece after every minor collection for a while, until there
are no more pieces.  The pieces are each doing a fraction of marking, or
a fraction of sweeping.

The main issue is that splitting the major collections means that the
main program is actually running between the pieces, and so can change
the pointers in the objects to point to other objects.  This is not
a problem for sweeping: dead objects will remain dead whatever the main
program does.  However, it is a problem for marking.  Let us see why.

In terms of the incremental GC literature, objects are either "white",
"gray" or "black".  They start as "white", become "gray" when they are
found to be alive, and become "black" when they have been fully
traversed --- at which point the objects that it points to have
themselves been marked gray, or maybe are already black.  The gray
objects are the "frontier" between the black objects that we have found
to be reachable, and the white objects that represent the unknown part
of the world.  When there are no more gray objects, the process is
finished: all remaining white objects are unreachable and can be freed
(by the following sweeping phase).

In this model, the important part is that a black object can never point
to a white object: if the latter remains white until the end, it will be
freed, which is incorrect because the black object itself can still be
reached.

The trick we used in PyPy is to consider minor collections as part of
the whole, rather than focus only on major collections.  The existing
minimark GC had always used a "write barrier" (a piece of code run every time
you set or get from an object or array) to do its job, like any
generational GC.  This write barrier is used to detect when an old
object (outside the nursery) is modified to point to a young object
(inside the nursery), which is essential information for minor
collections.  Actually, although this was the goal, the actual write
barrier code was simpler: it just recorded all old objects into which we
wrote *any* pointer --- to a young or old object.  It is actually a
performance improvement, because we don't need to check over and over
again if the written pointer points to a young object or not.

This *unmodified* write barrier works for incminimark too.  Imagine that
we are in the middle of the marking phase, running the main program.
The write barrier will record all old objects that are being modified.
Then at the next minor collection, all surviving young objects will be
moved out of the nursery.  At this point, as we're about to continue
running the major collection's marking phase, we simply add to the list
of pending gray objects all the objects that we consider --- both the
objects listed as "old objects that are being modified", and the objects
that we just moved out of the nursery.  A fraction of the former list
are turned back from the black to the gray color.  This technique
implements nicely, if indirectly, what is called a "backward write
barrier" in the literature: the backwardness is about the color that
occasionally progresses backward from black to gray.
