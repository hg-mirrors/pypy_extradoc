Multicore programming in Python
===============================

Hi all,

This is a short "position paper" kind of post about my view (Armin
Rigo's) on the future of multicore programming.  It is a summary of the
keynote presentation at EuroPython.  As I learned by talking with people
afterwards, I am not a good enough speaker to manage to convey a deeper
message in a 20-minutes talk.  I will try instead to convey it in a
150-lines post...

This is fundamentally about three points, which can be summarized as
follow:

1. We often hear about people wanting a version of Python running without
   the Global Interpreter Lock (GIL): a "GIL-less Python".  But what we
   programmers really need is not just a GIL-less Python --- we need a
   higher-level way to write multithreaded programs than using directly
   threads and locks.  One way is Automatic Mutual Exclusion (AME), which
   would give us an "AME Python".

2. A good enough Software Transactional Memory (STM) system can do that.
   This is what we are building into PyPy: an "AME PyPy".

3. The picture is darker for CPython, though there is a way too.  The
   problem is that when we say STM, we think about either GCC 4.7's STM
   support, or Hardware Transactional Memory (HTM).  However, both
   solutions are enough for a "GIL-less CPython", but not
   for "AME CPython", due to capacity limitations.  For the latter, we
   need somehow to add some large-scale STM into the compiler.

Let me explain these points in more details.


GIL-less versus AME
-------------------

The first point is in favor of the so-called Automatic Mutual Exclusion
approach.  The issue with using threads (in any language with or without
a GIL) is that threads are fundamentally non-deterministic.  In other
words, the programs' behaviors are not reproductible at all, and worse,
we cannot even reason about it --- it becomes quickly messy.  We would
have to consider all possible combinations of code paths and timings,
and we cannot hope to write tests that cover all combinations.  This
fact is often documented as one of the main blockers towards writing
successful multithreaded applications.

We need to solve this issue with a higher-level solution.  Such
solutions exist theoretically, and Automatic Mutual Exclusion (AME) is
one of them.  The idea of AME is that we divide the execution of each
thread into a number of "blocks".  Each block is well-delimited and
typically large.  Each block runs atomically, as if it acquired a GIL
for its whole duration.  The trick is that internally we use
Transactional Memory, which is a a technique that lets the interpreter
run the blocks from each thread in parallel, while giving the programmer
the illusion that the blocks have been run in some global serialized
order.

This doesn't magically solve all possible issues, but it helps a lot: it
is far easier to reason in terms of a random ordering of large blocks
than in terms of a random ordering of individual instructions.  For
example, a program might contain a loop over all keys of a dictionary,
performing some "mostly-independent" work on each value.  By using the
technique described here, putting each piece of work in one "block"
running in one thread of a pool, we get exactly the same effect: the
pieces of work still appear to run in some global serialized order, in
some random order (as it is anyway when iterating over the keys of a
dictionary).  There are even techniques building on top of AME that can
be used to force the order of the blocks, if needed.


PyPy and STM/AME
----------------

Talking more precisely about PyPy: the current prototype ``pypy-stm`` is
doing precisely this.  The length of the "blocks" above is selected in
one of two ways: either we have blocks corresponding to some small
number of bytecodes (in which case we have merely a GIL-less Python); or
we have blocks that are specified explicitly by the programmer using
``with thread.atomic:``.  The latter gives typically long-running
blocks.  It allows us to build the higher-level solution sought after:
it will run most of our Python code in multiple threads but always
within a ``thread.atomic`` block, e.g. using a pool of threads.

This gives the nice illusion of a global serialized order, and thus
gives us a well-behaving model of our program's behavior.  The drawback
is that we will usually have to detect and locate places that cause too
many "conflicts" in the Transactional Memory sense.  A conflict causes
the execution of one block of code to be aborted and restarted.
Although the process is transparent, if it occurs more than
occasionally, then it has a negative impact on performance.  We will
need better tools to deal with them.

The point here is that at any stage of this "improvement" process our
program is *correct*, while it may not be yet as efficient as it could
be.  This is the opposite of regular multithreading, where programs are
efficient but not as correct as they could be.  In other words, as we
all know, we only have resources to do the easy 80% of the work and not
the remaining hard 20%.  So in this model you get a program that has 80%
of the theoretical maximum of performance and it's fine.  In the regular
multithreading model we would instead only manage to remove 80% of the
bugs, and we are left with obscure rare crashes.


CPython and HTM
---------------

Couldn't we do the same for CPython?  The problem here is that, at
first, it seems we would need to change literally all places of the
CPython C sources in order to implement STM.  Here are our options:

- We could review and change code everywhere in CPython.

- We could use GCC 4.7, which supports some form of STM.

- We wait until Intel's next generation of CPUs comes out ("Haswell")
  and use HTM.

- We could write our own C code transformation (e.g. within a compiler
  like LLVM).

The first solution is a "thanks but no thanks".  If anything, it will
give another fork of CPython that is never going to be merged, that will
painfully struggle to keep not more than 3-4 versions behind, and that
will eventually die.

The issue with the next two solutions is the same one: both of these are
solutions that  small-scale transactions, but not long-running ones.  For
example, I have no clue how to give GCC rules about performing I/O in a
transaction --- this seems not supported at all; and moreover looking at
the STM library that is available so far to be linked with the compiled
program, it assumes short transactions only.

Intel's HTM solution is both more flexible and more strictly limited.
In one word, the transaction boundaries are given by a pair of special
CPU instructions that make the CPU enter or leave "transactional" mode.
If the transaction aborts, the CPU cancels any change, rolls back to the
"enter" instruction and causes this instruction to return an error code
instead of re-entering transactional mode (a bit like a ``fork()``).
The software then detects the error code; typically, if only a few
transactions end up being too long, it is fine to fall back to a
GIL-like solution just to do these transactions.

About the implementation: this is done by recording all the changes that
a transaction wants to do to the main memory, and keeping them invisible
to other CPUs.  This is "easily" achieved by keeping them inside this
CPU's local cache; rolling back is then just a matter of discarding a
part of this cache without committing it to memory.  From this point of
view, `there is a lot to bet`__ that we are actually talking about the
regular per-core Level 1 and Level 2 caches --- so any transaction that
cannot fully store its read and written data in the 64+256KB of the L1+L2
caches will abort.

.. __: http://arstechnica.com/business/2012/02/transactional-memory-going-mainstream-with-intel-haswell/

So what does it mean?  A Python interpreter overflows the L1 cache of
the CPU very quickly: just creating new Python function frames takes a
lot of memory (on the order of magnitude of 1/100 of the whole L1
cache).  Adding a 256KB L2 cache into the picture helps, particularly
because it is highly associative and thus avoids fake conflicts much
better.  However, as long as the HTM support is limited to L1+L2 caches,
it is not going to be enough to run an "AME Python" with any sort of
medium-to-long transaction (running for 0.01 second or longer).  It can
run a "GIL-less Python", though: just running a few hunderd or even
thousand bytecodes at a time should fit in the L1+L2 caches, for most
bytecodes.


Write your own STM for C
------------------------

Let's discuss now the last option: if neither GCC 4.7 nor HTM are
sufficient for an "AME CPython", then we might want to
write our own C compiler patch (as either extra work on GCC 4.7, or an
extra pass to LLVM, for example).

We would have to deal with the fact that we get low-level information,
and somehow need to preserve interesting high-level bits through the
compiler up to the point at which our pass runs: for example, whether
the field we read is immutable or not.  (This is important because some
common objects are immutable, e.g. PyIntObject.  Immutable reads don't
need to be recorded, whereas reads of mutable data must be protected
against other threads modifying them.)  We can also have custom code to
handle the reference counters: e.g. not consider it a conflict if
multiple transactions have changed the same reference counter, but just
resolve it automatically at commit time.  We are also free to handle I/O
in the way we want.

More generally, the advantage of this approach over the current GCC 4.7
is that we control the whole process.  While this still looks like a lot
of work, it looks doable.  It would be possible to come up with a
minimal patch of CPython that can be accepted into core without too much
troubles, and keep all the cleverness inside the compiler extension.


Conclusion?
-----------

I would assume that a programming model specific to PyPy and not
applicable to CPython has little chances to catch on, as long as PyPy is
not the main Python interpreter (which looks unlikely to change anytime
soon).  Thus as long as only PyPy has AME, it looks like it will not
become the main model of multicore usage in Python.  However, I can
conclude with a more positive note than during the EuroPython
conference: there appears to be a more-or-less reasonable way forward to
have an AME version of CPython too.
