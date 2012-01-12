Transactional Memory
====================

Here is an update about the previous blog post about the
`Global Interpreter Lock`__ (GIL).

.. __: http://morepypy.blogspot.com/p/global-interpreter-lock-or-how-to-kill.html

We believe we have a plan to implement an interesting model for using
multiple cores.  Believe it or not, this is *better* than just removing
the infamous GIL from PyPy.  You might get to use all your cores
*without ever writing threads.*

You would instead just use some event dispatcher, say from Twisted, from
Stackless, or from your favorite GUI; or just write your own.  In this
model, with minimal changes to the event dispatcher's source code ---
and of course by using a special version of PyPy --- you get some form
of automatic parallelization.  The basic idea is simple: start handling
multiple events in parallel, but give each one its own transaction_.

.. _transaction: http://en.wikipedia.org/wiki/Transactional_memory

Threads or Events?
------------------

First, why would this be better than "just" removing the GIL?  Because
using threads can be a mess in any complex program.  Some authors (e.g.
Lee_) have argued that the reason is that threads are fundamentally
non-deterministic.  This makes it very hard to reason about them.
Basically the programmer needs to "trim" down the non-determinism (e.g.
by adding locks, semaphores, etc.), and it's hard to be sure that he has
a sufficiently deterministic result, if only because he can't write
exhaustive tests for it.

.. _Lee: http://www.eecs.berkeley.edu/Pubs/TechRpts/2006/EECS-2006-1.pdf

By contrast, consider a Twisted program.  It's not a multi-threaded
program, which means that it handles the "events" one after the other.
The exact ordering of the events is not really deterministic, because
they often correspond to external events; but that's the only source of
non-determinism.  The actual handling of each event occurs in a nicely
deterministic way, and most importantly, not in parallel with the
handling of other events.  The same is true about other libraries like
GUI toolkits, gevent, or even Stackless.

These two models --- threads or events --- are the two main models we
have right now.  The latter is more used in Python, because it is much
simpler to use than the former, and the former doesn't give any benefit
because of the GIL.  A third model, which is the only one that gives
multi-core benefits, is to use multiple processes, and do inter-process
communication.

The problem
-----------

Consider the case of a big program that has arbitrary complicated
dependencies.  Even assuming a GIL-less Python, this is likely enough to
prevent the programmer from even starting a multi-threaded rewrite,
because it would require a huge mess of locks.  He could also consider
using multiple processes instead, but the result is annoying too: the
complicated dependencies translate into a huge mess of inter-process
synchronization.

The problem can also be down-sized to very small programs, like the kind
of hacks that you do and forget about.  In this case, the dependencies
might be simpler, but you still have to learn and use a complex
inter-process library, which is overkill for the purpose.  I would even
argue that this is similar to how we might feel a priori that automatic
memory management is overkill in small programs --- of course anyone who
wrote a number of 15-line Python scripts knows this to be wrong.  This
is even *so* wrong that the opposite is obvious nowadays: it makes no
sense whatsoever to manage object lifetimes explicitly in most small
scripts.  I think the same will eventually be true for using multiple
CPUs.

Events in Transactions
----------------------

Consider again the Twisted example I gave above.  The case I am
interested in is the case in which events are *generally mostly
independent.*  By this I mean the following: there are often several
events pending in the dispatch queue (assuming the program is not under
100% 1-CPU load, otherwise the whole discussion is moot).  Handling
these events is often mostly independent --- but the point is that they
don't *have* to be proved independent.  In fact it is fine if they have
arbitrary complicated dependencies as described above.  The point is the
expected common case.  Imagine that you have a GIL-less Python and that
you can, by a wave of your hand, have all the careful locking mess
magically done.  Then what I mean here is the case in which this
theoretical program would run mostly in parallel on multiple core,
without waiting too often on the locks.

In this case, with minimal tweaks in the event dispatch loop, we can
handle multiple events on multiple threads, each in its own transaction.
A transaction is basically a tentative execution of the corresponding
piece of code: if we detect conflicts with other concurrently executing
transactions, we cancel the whole transaction and restart it from
scratch.

By now, the fact that it can basically work should be clear: multiple
transactions will only get into conflicts when modifying the same data
structures, which is the case where the magical wand above would have
put locks.  If the magical program could progress without too many
locks, then the transactional program can progress without too many
conflicts.  Moreover, you get more than what the magical program can
give you: each event is dispatched in its own transaction, which means
that from each event's point of view, we have the illusion that nobody
else is running concurrently.  This is exactly what all existing
Twisted-/Stackless-/etc.-based programs are assuming.

xxx
