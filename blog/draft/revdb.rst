Hi all,

If I had to pick the main advantage of PyPy over CPython, it is that
we have got with the RPython translation toolchain a real place for
experimentation.  Every now and then, we build inside RPython some
feature that gives us an optionally tweaked version of the PyPy
interpreter---tweaked in a way that would be hard to do with CPython,
because it would require systematic changes everywhere.  The most
obvious and successful examples are the GC and the JIT.  But there
have been many other experiments along the same lines, from the
so-called "stackless transformation" in the early days, to the STM
version of PyPy.

Today I would like to present you with last month's work (still very
much in alpha state).  It is a RPython transformation that gives
support for a *reverse debugger* in PyPy or in any other interpreter
written in RPython.


Reverse debugging
-----------------

What is `reverse debugging`__?  It is a debugger where you can go
forward and backward in time.  It is still a not commonly used
feature, and I have no idea why not.  I have used UndoDB's reverse
debugger for C code, and I can only say that it saved me many, many
days of poking around blindly in gdb.

.. __: https://en.wikipedia.org/wiki/Debugger#Reverse_debugging

There are already some Python experiments about reverse debugging.
However, I claim that they are not very useful.  How they work is
typically by recording changes to some objects, like lists and
dictionaries, in addition to recording the history of where your
program passed through.  However, the problem of Python is, again,
that lists and dictionaries are not the end of the story.  There are
many, many, many types of objects written in C which are mutable---in
fact, the immutable ones are the exception.  You can try to
systematically record all changes, but it is a huge task and easy to
forget a detail.

In other words it is a typical use case for tweaking the RPython
translation toolchain rather than the CPython or PyPy interpreter
directly.


RevDB in PyPy
-------------

Right now, RevDB works barely enough to start being useful.  I have
used it to track one real bug (for the interested people, see
bd220c268bc9_).  So here is what it is, what it is not, and how to use
it.

.. _bd220c268bc9: https://bitbucket.org/pypy/pypy/commits/bd220c268bc9

RevDB is a Python debugger.  It will not help track issues like
segfaults or crashes of the interpreter, but it will help track any
Python-level bugs.  Think about bugs that end up as a Python traceback
or another wrong answer, but where the problem is really caused by
something earlier going wrong in your Python logic.

RevDB is a logging system, similar to http://rr-project.org/ .  You
first run your Python program by using a special version of PyPy.  It
creates a log file which records the I/O actions.  Sometimes you are
tracking a rare bug: you may need to run your program many times until
it shows the crash.  That should still be reasonable: the special
version of PyPy is very slow (it does not contain any JIT nor one of
our high-performance GCs), but still not incredibly so---it is a few
times slower than running the same program on CPython.  The point is
also that normally, what you need is just one recorded run of the
program showing the bug.  You may struggle a bit to get that, but once
you have it, this part is done.

Then you use the debugger on the log file.  The debugger will also
internally re-run the special version of PyPy in a different mode.
This feels like a debugger, though it is really a program that
inspects any point of the history.  Like in a normal pdb, you can use
commands like "next" and "p foo.bar" and even run more complicated
bits of Python code.  You also have new commands like "bnext" to go
backwards.  Most importantly, you can set *watchpoints*.  More about
that later.


XXX CF: it's not clear to me what "doing any input/output from the debugger" means

What you cannot do is do any input/output from the debugger.  Indeed,
the log file records all imports that were done and what the imported
modules contained.  Running the debugger on the log file gives an
exact replay of what was recorded.










- no thread module for now.  And, no cpyext module for now (the
  CPython C API compatibility layer), because it depends on threads.
  No micronumpy either.
  These missing modules are probably blockers for large programs.

- does not contain a JIT, and does not use our fast garbage collector.

- for now, the process needs to get the same addresses (of C functions
  and static data) when recording and when replaying.  On the Linux I
  tried it with, you get this result by disabling Address Space Layout
  Randomization (ASLR)::

       echo 0 | sudo tee /proc/sys/kernel/randomize_va_space

- OS/X and other Posix platforms are probably just a few fixes away.
  Windows support will require some custom logic to replace the
  forking done when replaying.  This is more involved but should still
  be possible.

- maybe 15x memory usage on replaying (adjust number of forks in
  process.py, MAX_SUBPROCESSES).

- replaying issues:

  - Attempted to do I/O or access raw memory: we get this often, and
    then we need "bstep+step" before we can print anything else

  - id() is globally unique, returning a reproducible 64-bit number,
    so sometimes using id(x) is a workaround for when using x doesn't
    work because of "Attempt to do I/O" issues (e.g.
    ``p [id(x) for x in somelist]``)

  - next/bnext/finish/bfinish might jump around a bit non-predictably.

  - similarly, breaks on watchpoints can stop at apparently unexpected
    places (when going backward, try to do "step" once).  The issue is
    that it can only stop at the beginning of every line.  In the
    extreme example, if a line is ``foo(somelist.pop(getindex()))``,
    then ``somelist`` is modified in the middle.  Immediately before
    this modification occurs, we are in ``getindex()``, and
    immediately afterwards we are in ``foo()``.  The watchpoint will
    stop the program at the end of ``getindex()`` if running backward,
    and at the start of ``foo()`` if running forward, but never
    actually on the line doing the change.

  - the first time you use $NUM to refer to an object, if it was
    created long ago, then replaying might need to replay again from
    that long-ago time
