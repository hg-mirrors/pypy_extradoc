Global Interpreter Lock, or how to kill it
==========================================

People that listened to my lightning talk at EuroPython know that
(suddenly) we have a plan to remove the Global Interpreter Lock --- the
infamous GIL, the thing in CPython that prevents multiple threads from
actually running in your Python code in parallel.

That's not actually new, because Jython has been doing it all along (and
I think IronPython too).  Jython works by very carefully adding locks to
all the mutable built-in types, and by relying on the underlying Java
platform to be efficient about them (so that the result is faster than,
say, very carefully adding similar locks in CPython).  By "very
carefully", I mean *really* *really* carefully; for example,
'dict1.update(dict2)' needs to lock both dict1 and dict2, but if you do
it naively, then a parallel 'dict2.update(dict1)' might cause a
deadlock.

We are considering a quite different approach, based on `Software
Transactional Memory`_.  This is a recent development in computer
science, and it gives a nicer solution than locking.  Here is a short
introduction to it.

Say you want to atomically pop an item from 'list1' and append it to
'list2'::

    def f(list1, list2):
        x = list1.pop()
        list2.append(x)

This is not safe in multithreaded cases (even with the GIL).  Say that
you call ``f(l1, l2)`` in thread 1 and ``f(l2, l1)`` in thread 2.  What
you want is that it has no effect at all (x is moved from one list to
the other, then back).  But what can occur is that instead the top of
the two lists are swapped, depending on timing issues.

One way to fix it is with a global lock::

    def f(list1, list2):
        global_lock.acquire()
        x = list1.pop()
        list2.append(x)
        global_lock.release()

A finer way to fix it is with locks that come with the lists::

    def f(list1, list2):
        acquire_all_locks(list1.lock, list2.lock)
        x = list1.pop()
        list2.append(x)
        release_all_locks(list1.lock, list2.lock)

The second solution is a model for Jython's, while the first is a model
for CPython's.  Indeed, in CPython's interpreter, we acquire the GIL,
then we do one bytecode (or actually a number of them, like 100), then
we release the GIL; and then we proceed to the next bunch of 100.

Software Transactional Memory (STM) gives a third solution::

    def f(list1, list2):
        while True:
            t = transaction()
            x = list1.pop(t)
            list2.append(t, x)
            if t.commit():
                break

In this solution, we make a ``transaction`` object and use it in all
reads and writes we do to the lists.  There are actually several
different models, but let's focus on one of them.  During a transaction,
we don't actually change the global memory at all.  Instead, we use the
thread-local ``transaction`` object.  We store in it which objects we
read from, which objects we write to, and what values we write.  It is
only when the transaction reaches its end that we attempt to "commit"
it.  Committing might fail if other commits have occurred in between,
creating inconsistencies; in that case, the transaction aborts and
must restart from the beginning.

In the same way as the previous two solutions are models for CPython and
Jython, the STM solution looks like it could be a model for PyPy in the
future.  In such a PyPy, the interpreter would start a transaction, do
one or several bytecodes, and then end the transaction; and repeat.
This is very similar to what is going on in CPython with the GIL.  In
particular, it means that it gives programmers all the same guarantees
as the GIL does.  The *only* difference is that it can actually run
multiple threads in parallel, as long as their code does not interfere
with each other.  

XXX how much slower would it make things for the person whose code
isn't suitable to try to run it?  All of us?  Is this an option you
could enable?

Why not apply that idea to CPython?  Because we would need to change
everything everywhere.  In the example above, you may have noted that I
no longer call 'list1.pop()', but 'list1.pop(t)'; this is a way to tell
that the implementation of all the methods needs to be changed, in order
to do their work "transactionally".  This means that instead of really
changing the global memory in which the list is stored, it must instead
record the change in the ``transation`` object.  If our interpreter is
written in C, as CPython is, then we need to write it explicitly
everywhere.  If it is written instead in a higher-level language, as
PyPy is, then we can add this behavior as as set of translation rules, and 
apply them automatically wherever it is necessary.

A final note: as STM research is very recent (it started around 2003),
there are a number of variants around, and it's not clear yet which one
is better in which cases.  As far as I can tell, the approach described
in "A Comprehensive Strategy for Contention Management in Software
Transactional Memory" seems to be one possible state-of-the-art; it also
seems to be "good enough for all cases".

So, when will it be done?  No clue so far.  It is still at the idea
stage, but I *think* that it can work.  How long would it take us to
write it?  Again no clue, but we are looking at many months rather
than many days.  This is the sort of thing that I (Armin Rigo) would
like to be able to work on full time after the `Eurostars funding`_
runs out on September 1.  We are currently looking at ways to use
`crowdfunding`_ to raise money so that I can do exactly that.  Expect
a blog post about that very soon.  But this looks like a perfect
candidate for crowdfunding -- there are at least thousands of you who
would be willing to pay 10s of Euros to Kill the Gil.  Now we only
have to make this happen.


.. _`Software Transactional Memory`: http://en.wikipedia.org/wiki/Software_transactional_memory
.. _`this paper`: 
.. _`Eurostars funding`: http://morepypy.blogspot.com/2010/12/oh-and-btw-pypy-gets-funding-through.html
.. _`crowdfunding`:http://en.wikipedia.org/wiki/Crowd_funding