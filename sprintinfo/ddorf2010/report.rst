Düsseldorf Sprint Report 2010
==============================

This years installment of the yearly PyPy Düsseldorf Sprint is drawing to a
close. As usual, we worked in the seminar room of the `programming language
group`_ at the University of Düsseldorf. The sprint was different from previous
ones in that we had fewer people than usual and many actually live in
Düsseldorf all the time. 

David spent the sprint working on the `arm-backend`_ branch, which is adding an
ARM backend to the JIT. With the help of Armin he added support for bridges in
the JIT and generally implemented missing operations, mostly for handling integers so far.

.. _`arm-backend`: http://codespeak.net/svn/pypy/branch/arm-backend/

Ronny and Anto worked the whole week trying to come up with a scheme for
importing PyPy's SVN history into a mercurial repository without loosing too
much information. This is a non-trivial task, because PyPy's history is gnarly.
We are nearly at revision 79000 and when we started using it, Subversion was at
version 0.1. All possible and impossible ways to mangle and mistreat a
Subversion repository have been applied to PyPy's repo, so most of the
importing tools just give up. Ronny and Anto came up with a new plan and new
helper scripts every day, only to then discover another corner case that they
hadn't thought of. Now they might actually have a final plan (but they said
that every day, so who knows?).

Carl Friedrich and Lukas started working in earnest on memory benchmarks to
understand the memory behaviour of Python code better. They have now
implemented a generic memory benchmark runner and a simple analysis that walks
all objects and collects size information about them. They also added some
benchmarks that were proposed in the comments of the recent `call for
benchmarks`_. As soon as some results from that work are there, we will post
about them.

.. _`call for benchmarks`: http://morepypy.blogspot.com/2010/08/call-for-benchmarks.html

There were also some minor tasks performed during the sprint. Armin implemented
the ``_bisect`` module and the ``dict.popitem`` method in RPython. Armin and
Carl Friedrich made the new memory-saving mapdict implementation more suitable
to use without the JIT (blog post should come about that too, at some point).
They also made classes with custom metaclasses a lot faster when the JIT is
used.

The last three days of the sprint were spent working on Håkan's
`jit-unroll-loops`_ branch.  The branch is meant to move loop invariants out of
the loop, using techniques very similar to what is described in the recent post
on `escape analysis across loop boundaries`_ (see? it will soon stop being
science-fiction). Some of the ideas of this approach also come from LuaJIT_
which also uses very aggressive loop invariant code motion in its optimizers.
Moving loop invariants outside of the loop is very useful, because many of the
lookups that Python programs do in loops are loop invariants. An example is if
you call a function in a loop: The global lookup can often be done only once. 

This branch fundamentally changes some of the core assumptions of the JIT, so
it is a huge amount of work to make it fit with all the other parts and to
adapt all tests. That work is now nearly done, some failing tests remain. The
next steps are to fix them and then do additional tests with the translated
executable and look at the benchmarks.

.. _`jit-unroll-loops`: http://codespeak.net/svn/pypy/branch/jit-unroll-loops/
.. _`escape analysis across loop boundaries`: http://morepypy.blogspot.com/2010/09/using-escape-analysis-across-loop.html
.. _LuaJIT: http://luajit.org/
