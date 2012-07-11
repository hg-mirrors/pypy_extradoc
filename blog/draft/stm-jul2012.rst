STM/AME future in CPython and PyPy
==================================

Hi all,

This is a short "position paper" kind of post about my view (Armin
Rigo's) on the future of multicore programming.  It is a summary of the
keynote presentation at EuroPython.  As I learned by talking with people
afterwards, I am not a good enough speaker to manage to convey a deeper
message in a 20-minutes talk.  I will try instead to convey it in a
150-lines post :-)

This is fundamentally about three points, which can be summarized as
follow:

1. We often hear about people wanting a version of Python running without
   the Global Interpreter Lock (GIL): a "GIL-less Python".  But what we
   programmers really need is not just a GIL-less Python --- it is a
   higher-level way to write multithreaded programs.  This can be
   achieved with Automatic Mutual Exclusion (AME): an "AME Python".

2. A good enough Software Transactional Memory (STM) system can do that.
   This is what we are building into PyPy: an "AME PyPy".

3. The picture is darker for CPython.  The only viable solutions there
   are GCC's STM support, or Hardware Transactional Memory (HTM).
   However, both solutions are enough for a "GIL-less CPython", but not
   for "AME CPython", due to capacity limitations.

Before we come to conclusions, let me explain these points in more
details.


GIL-less versus AME
-------------------

The first point is in favor of the so-called Automatic Mutual Exclusion
approach.  The issue with using threads (in any language with or without
a GIL) is that threads are fundamentally non-deterministic.  In other
words, the programs' behavior is not reproductible at all, and worse, we
cannot even reason about it --- it becomes quickly messy.  We would have
to consider all possible combinations of code paths and timings, and we
cannot hope to write tests that cover all combinations.  This fact is
often documented as one of the main blockers towards writing successful
multithreaded applications.

We need to solve this issue with a higher-level solution.  Such
solutions exist theoretically, and Automatic Mutual Exclusion is one of
them.  The idea is that we divide the execution of each thread into some
number of large, well-delimited blocks.  Then we use internally a
technique that lets the interpreter run the threads in parallel, while
giving the programmer the illusion that the blocks have been run in some
global serialized order.


PyPy and STM
------------

Talking more precisely about PyPy: the current prototype ``pypy-stm`` is
doing precisely this.  The length of the "blocks" above is selected in
one of two ways: either we have blocks corresponding to some small
number of bytecodes (in which case we have merely a GIL-less Python); or
we have blocks that are specified explicitly by the programmer using
``with thread.atomic:``.  The latter gives typically long-running
blocks.  It allows us to build the higher-level solution sought after:
we will run most of our Python code in multiple threads but always
within a ``thread.atomic``.

This gives the nice illusion of a global serialized order, and thus
gives us a well-behaving model of our program's behavior.  Of course, it
is not the perfect solution to all troubles: notably, we have to detect
and locate places that cause too many "conflicts" in the Transactional
Memory sense.  A conflict causes the execution of one block of code to
be aborted and restarted.  Although the process is transparent, if it
occurs more than occasionally, then it has a negative impact on
performance.  We will need better tools to deal with them.  The point
here is that at all stages our program is *correct*, while it may not be
as efficient as it could be.  This is the opposite of regular
multithreading, where programs are efficient but not as correct as they
could be...


CPython and HTM
---------------

Couldn't we do the same for CPython?  The problem here is that we would
need to change literally all places of the CPython C sources in order to
implement STM.  Assuming that this is far too big for anyone to handle,
we are left with two other options:

- We could use GCC 4.7, which supports some form of STM.

- We wait until Intel's next generation of CPUs comes out ("Haswell")
  and use HTM.

The issue with each of these two solutions is the same: they are meant
to support small-scale transactions, but not long-running ones.  For
example, I have no clue how to give GCC rules about performing I/O in a
transaction; and moreover looking at the STM library that is available
so far to be linked with the compiled program, it assumes short
transactions only.

Intel's HTM solution is both more flexible and more strictly limited.
In one word, the transaction boundaries are given by a pair of special
CPU instructions that make the CPU enter or leave "transactional" mode.
If the transaction aborts, the CPU rolls back to the "enter" instruction
(like a ``fork()``) and causes this instruction to return an error code
instead of re-entering transactional mode.  The software then detects
the error code; typically, if only a few transactions end up being too
long, it is fine to fall back to a GIL-like solution just to do these
transactions.

This is all implemented by keeping all changes to memory inside the CPU
cache, invisible to other cores; rolling back is then just a matter of
discarding a part of this cache without committing it to memory.  From
this point of view, there is a lot to bet that this cache is actually
the regular per-core Level 1 cache --- any transaction that cannot fully
store its read and written data in the 32-64KB of the L1 cache will
abort.

So what does it mean?  A Python interpreter overflows the L1 cache of
the CPU almost instantly: just creating new frames takes a lot of memory
(the order of magnitude is below 100 function calls).  This means that
as long as the HTM support is limited to L1 caches, it is not going to
be enough to run an "AME Python" with any sort of medium-to-long
transaction.  It can run a "GIL-less Python", though: just running a few
bytecodes at a time should fit in the L1 cache, for most bytecodes.


Conclusion?
-----------

Even if we assume that the arguments at the top of this post are valid,
there is more than one possible conclusion we can draw.  My personal
pick in the order of likeliness would be: people might continue to work
in Python avoiding multiple threads, even with a GIL-less interpreter;
or they might embrace multithreaded code and some half-reasonable tools
and practices might emerge; or people will move away from Python in
favor of a better suited language; or finally people will completely
abandon CPython in favor of PyPy (but somehow I doubt it :-)

I will leave the conclusions open, as it basically depends on a language
design issue and so not my strong point.  But if I can point out one
thing, it is that the ``python-dev`` list should discuss this issue
sooner rather than later.
