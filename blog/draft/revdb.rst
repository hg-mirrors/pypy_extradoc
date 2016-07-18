============================
Reverse debugging for Python
============================

RevPDB
------

A "reverse debugger" is a debugger where you can go forward and
backward in time.  It is an uncommon feature, at least in the open
source world, but I have no idea why.  I have used `undodb-gdb`_ and
`rr`_, which are reverse debuggers for C code, and I can only say that
they saved me many, many days of poking around blindly in gdb.

The PyPy team is pleased to give you "RevPDB", a reverse-debugger
similar to ``rr`` but for Python.

An example is worth a thousand words.  Let's say your big Python
program has a bug that shows up inconsistently.  You have nailed it
down to something like:

* start ``x.py``, which does stuff (maybe involving processing files,
  answering some web requests that you simulate from another terminal,
  etc.);

* sometimes, after a few minutes, your program's state becomes
  inconsistent and you get a failing assert or another exception.

This is the case where RevPDB is useful.

RevPDB is only available only on 64-bit Linux right now, but should
not be too hard to port to other OSes.  It is very much *alpha-level!*
(It is a debugger full of bugs.  Sorry about that.)  I believe it is
still useful---it helped me in one `real use case`_ already.

.. _`real use case`: https://bitbucket.org/pypy/pypy/commits/bd220c268bc9


How to get RevPDB
-----------------

The following demo was done with an alpha version for 64-bit Linux,
compiled for Arch Linux.  I won't provide the binary; it should be
easy enough to retranslate (much faster than a regular PyPy because it
contains neither a JIT nor a custom GC).  Grab the `PyPy sources`_ from
Mercurial, and then::

    hg update reverse-debugger   # this demo done with "hg update 4d82621df5ed"
    cd pypy/goal
    ../../rpython/bin/rpython -O2 --revdb targetpypystandalone.py --withoutmod-cpyext --withoutmod-micronumpy

and possibly rename the final ``pypy-c`` to ``pypy-revdb`` to avoid
confusion.

Other platforms than 64-bit Linux need some fixes before they work.

.. _`PyPy sources`: http://pypy.org/download.html#building-from-source


Demo
----

For this demo, we're going to use this ``x.py`` as the "big program"::

    import os

    class Foo(object):
        value = 5

    lst1 = [Foo() for i in range(100)]
    lst1[50].value += 1
    for x in lst1:
        x.value += 1

    for x in lst1:
        if x.value != 6:
            print 'oops!'
            os._exit(1)

Of course, it is clear what occurs in this small example: the check
fails on item 50.  For this demo, the check has been written with
``os._exit(1)``, because this exits immediately the program.  If it
was written with an ``assert``, then its failure would execute things
in the ``traceback`` module afterwards, to print the traceback; it
would be a minor mess just to find the exact point of the failing
``assert``.  (This and other issues are supposed to be fixed in the
future, but for now it is alpha-level.)

Anyway, with a regular ``assert`` and a regular post-mortem ``pdb``,
we could observe that ``x.value`` is indeed 7 instead of 6 when the
assert fails.  Imagine that the program is much bigger: how would we
find the exact chain of events that caused this value 7 to show up on
this particular ``Foo`` object?  This is what RevPDB is for.

First, we need for now to disable Address Space Layout Randomization
(ASLR), otherwise replaying will not work.  This is done once with the
following command line, which changes the state until the next
reboot::

    echo 0 | sudo tee /proc/sys/kernel/randomize_va_space

Run ``x.py`` with RevPDB's version of PyPy instead of the regular
interpreter (CPython or PyPy)::

    PYPYRDB=log.rdb ./pypy-revdb x.py

This ``pypy-revdb`` executable is like a slow PyPy executable, running
(for now) without a JIT.  This produces a file ``log.rdb`` which
contains a complete log of this execution.  (If the bug we are
tracking occurs rarely, we need to re-run it several times until we
get the failure.  But once we got the failure, then we're done with
this step.)

Start::
    
    rpython/translator/revdb/revdb.py log.rdb
    
We get a pdb-style debugger.  This ``revdb.py`` is a normal Python
program, which you run with an unmodified Python; internally, it looks
inside the log for the path to ``pypy-revdb`` and run it as needed (as
one forking subprocess, in a special mode).

Initially, we are at the start of the program---not at the end, like
we'd get in a regular debugger::

    File "<builtin>/app_main.py", line 787 in setup_bootstrap_path:
    (1)$

The list of commands is available with ``help``.

Go to the end with ``continue`` (or ``c``)::
  
    (1)$ continue
    File "/tmp/x.py", line 14 in <module>:
    ...
      lst1 = [Foo() for i in range(100)]
      lst1[50].value += 1
      for x in lst1:
          x.value += 1

      for x in lst1:
          if x.value != 6:
              print 'oops!'
    >         os._exit(1)
    (19727)$

We are now at the beginning of the last executed line.  The number
19727 is the "time", measured in number of lines executed.  We can go
backward with the ``bstep`` command (backward step, or ``bs``), line
by line, and forward again with the ``step`` command.  There are also
commands ``bnext``, ``bcontinue`` and ``bfinish`` and their forward
equivalents.  There is also "``go TIME``" to jump directly to the specified
time.  (Right now the debugger only stops at "line start"
events, not at function entry or exit, which makes some cases a bit
surprising: for example, a ``step`` from the return statement of
function ``foo()`` will jump directly to the caller's caller, if the
caller's current line was ``return foo() + 2``, because no "line
start" event occurs in the caller after ``foo()`` returns to it.)

We can print Python expressions and statements using the ``p``
command::

    (19727)$ p x
    $0 = <__main__.Foo object at 0xfffffffffffeab3e>
    (19727)$ p x.value
    $1 = 7
    (19727)$ p x.value + 1
    8

The "``$NUM =``" prefix is only shown when we print an object that
really exists in the debugged program; that's why the last line does
not contain it.  Once a ``$NUM`` has been printed, then we can use
it in further expressions---even at a different point time.  It
becomes an anchor that always refers to the same object::

    (19727)$ bstep

    File "/tmp/x.py", line 13 in <module>:
    ...

      lst1 = [Foo() for i in range(100)]
      lst1[50].value += 1
      for x in lst1:
          x.value += 1

      for x in lst1:
          if x.value != 6:
    >         print 'oops!'
              os._exit(1)
    (19726)$ p $0.value
    $1 = 7

In this case, we want to know when this value 7 was put in this
attribute.  This is the job of a watchpoint::

    (19726)$ watch $0.value
    Watchpoint 1 added
    updating watchpoint value: $0.value => 7
    
This watchpoint means that ``$0.value`` will be evaluated at each line.
When the ``repr()`` of this expression changes, the watchpoint activates
and execution stops::

    (19726)$ bcontinue
    [searching 19629..19726]
    [searching 19338..19629]

    updating watchpoint value: $0.value => 6
    Reverse-hit watchpoint 1: $0.value
    File "/tmp/x.py", line 9 in <module>:
      import os

      class Foo(object):
          value = 5

      lst1 = [Foo() for i in range(100)]
      lst1[50].value += 1
      for x in lst1:
    >     x.value += 1

      for x in lst1:
          if x.value != 6:
              print 'oops!'
              os._exit(1)
    (19524)$

Note that using the ``$NUM`` syntax is essential in watchpoints.  You
can't say "``watch x.value``", because the variable ``x`` will go out
of scope very soon when we move forward or backward in time.  In fact
the watchpoint expression is always evaluated inside an environment
that contains the builtins but not the current locals and globals.
But it also contains all the ``$NUM``, which can be used to refer to
known objects.  It is thus common to watch ``$0.attribute`` if ``$0``
is an object, or to watch ``len($1)`` if ``$1`` is some list.  The
watch expression can also be a simple boolean: for example, "``watch
$2 in $3``" where ``$3`` is some dict and ``$2`` is some object that
you find now in the dict; you would use this to find out the time when
``$2`` was put inside ``$3``, or removed from it.

Use "``info watchpoints``" and "``delete <watchpointnum>``" to manage
watchpoints.

There are also regular breakpoints, which you set with "``b
FUNCNAME``".  It breaks whenever there is a call to a function that
happens to have the given name.  (It might be annoying to use for a
function like ``__init__()`` which has many homonyms.  There is no
support for breaking on a fully-qualified name or at a given line
number for now.)

In our demo, we stop at the line ``x.value += 1``, which is where the
value was changed from 6 to 7.  Use ``bcontinue`` again to stop at the
line ``lst1[50].value += 1``, which is where the value was changed from
5 to 6.  Now we know how this ``value`` attribute ends up being 7.

::

    (19524)$ bcontinue
    [searching 19427..19524]
    [searching 19136..19427]

    updating watchpoint value: $0.value => 5
    Reverse-hit watchpoint 1: $0.value
    File "/tmp/x.py", line 7 in <module>:
      import os

      class Foo(object):
          value = 5

      lst1 = [Foo() for i in range(100)]
    > lst1[50].value += 1
      for x in lst1:
          x.value += 1

      for x in lst1:
          if x.value != 6:
    ...
    (19422)$

Try to use ``bcontinue`` yet another time.  It will stop now just before
``$0`` is created.  At that point in time, ``$0`` refers to
an object that does not exist yet, so the watchpoint now evaluates to
an error message (but it continues to work as before, with that error
message as the string it currently evaluates to).

::

    (19422)$ bcontinue
    [searching 19325..19422]

    updating watchpoint value: $0.value => RuntimeError:
            '$0' refers to an object created later in time
    Reverse-hit watchpoint 1: $0.value
    File "/tmp/x.py", line 6 in <module>:
      import os

      class Foo(object):
          value = 5

    > lst1 = [Foo() for i in range(100)]
      lst1[50].value += 1
      for x in lst1:
          x.value += 1

      for x in lst1:
    ...
    (19371)$ 

In big programs, the workflow is similar, just more complex.  Usually
it works this way: we find interesting points in time with some
combination of watchpoints and some direct commands to move around.
We write down on a piece of (real or virtual) paper these points in
history, including most importantly their time, so that we can
construct an ordered understanding of what is going on.

The current ``revdb`` can be annoying and sometimes even crash; but
the history you reconstruct can be kept.  All the times and
expressions printed are still valid when you restart ``revdb``.  The
only thing "lost" is the ``$NUM`` objects, which you need to print
again.  (Maybe instead of ``$0``, ``$1``, ...  we should use ``$<big
number>``, where the big number identifies uniquely the object by its
creation time.  These numbers would continue to be valid even after
``revdb`` is restarted.  They are more annoying to use than just
``$0`` though.)


Current issues
--------------

General issues:

* If you are using ``revdb`` on a log that took more than a few
  minutes to record, then it can be painfully slow.  This is because
  ``revdb`` needs to replay again big parts of the log for some
  operations.

* The ``pypy-revdb`` is currently missing the following modules:

  - ``thread`` (implementing multithreading is possible, but not done
    yet);

  - ``cpyext`` (the CPython C API compatibility layer);

  - ``micronumpy`` (minor issue only);

  - ``_continuation`` (for greenlets).

* Does not contain a JIT, and does not use our fast garbage
  collectors.  You can expect ``pypy-revdb`` to be maybe 3 times
  slower than CPython.

* Only works on Linux, and only with Address Space Layout
  Randomization (ASLR) disabled.  There is no fundamental reason for
  either restriction, but it is some work to fix.

* Replaying a program uses a *lot* more memory; maybe 15x as much than
  during the recording.  This is because it creates many forks.  If
  you have a program that consumes 10% of your RAM or more, you will
  need to reduce ``MAX_SUBPROCESSES`` in ``process.py``.

Replaying also comes with a bunch of user interface issues:

- ``Attempted to do I/O or access raw memory``: we get this whenever
  trying to ``print`` some expression that cannot be evaluated with
  only the GC memory---or which can, but then the ``__repr__()``
  method of the result cannot.  We need to reset the state with
  ``bstep`` + ``step`` before we can print anything else.  However,
  if only the ``__repr__()`` crashes, you still see the ``$NUM =``
  prefix, and you can use that ``$NUM`` afterwards.

- ``id()`` is globally unique, returning a reproducible 64-bit number,
  so sometimes using ``id(x)`` is a workaround for when using ``x``
  doesn't work because of ``Attempted to do I/O`` issues (e.g.  ``p
  [id(x) for x in somelist]``).

- as explained in the demo, next/bnext/finish/bfinish might jump
  around a bit non-predictably.

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

- watchpoint expressions *must not* have any side-effect at all.  If
  they do, the replaying will get out of sync and ``revdb.py`` will
  complain about that.  Regular ``p`` expressions and statements can
  have side-effects; these effects are discarded as soon as you move
  in time again.

- sometimes even "``p import foo``" will fail with ``Attempted to do
  I/O``.  Use instead "``p import sys; foo = sys.modules['foo']``".

- use ``help`` to see all commands.  ``backtrace`` can be useful.
  There is no ``up`` command; you have to move in time instead,
  e.g. using ``bfinish`` to go back to the point where the current
  function was called.


How RevPDB is done
------------------

If I had to pick the main advantage of PyPy over CPython, it is that
we have got with the RPython translation toolchain a real place for
experimentation.  Every now and then, we build inside RPython some
feature that gives us an optionally tweaked version of the PyPy
interpreter---tweaked in a way that would be hard to do with CPython,
because it would require systematic changes everywhere.  The most
obvious and successful examples are the GC and the JIT.  But there
have been many other experiments along the same lines, from the
so-called `stackless transformation`_ in the early days, to the STM
version of PyPy.

.. _`stackless transformation`: https://bitbucket.org/pypy/extradoc/raw/tip/eu-report/D07.1_Massive_Parallelism_and_Translation_Aspects-2007-02-28.pdf

RevPDB works in a similar way.  It is a version of PyPy in which some
operations are systematically replaced with other operations.

To keep the log file at a reasonable size, we duplicate the content of
all GC objects during replaying---by repeating the same actions on
them, without writing anything in the log file.  So that means that in
the ``pypy-revdb`` binary, the operations that do arithmetic or
read/write GC-managed memory are not modified.  Most operations are
like that.  However, the other operations, the ones that involve
either non-GC memory or calls to external C functions, are tweaked.
Each of these operations is replaced with code that works in two
modes, based on a global flag:

* in "recording" mode, we log the result of the operation (but not the
  arguments);

* in "replaying" mode, we don't really do the operation at all, but
  instead just fetch the result from the log.

Hopefully, all remaining unmodified operations (arithmetic and GC
load/store) are completely deterministic.  So during replaying, every
integer or non-GC pointer variable will have exactly the same value as
it had during recording.  Interestingly, it means that if the
recording process had a big array in non-GC memory, then in the
replaying process, the array is not allocated at all; it is just
represented by the same address, but there is nothing there.  When we
record "read item 123 from the array", we record the result of the
read (but not the "123").  When we replay, we're seeing again the same
"read item 123 from the array" operation.  At that point, we don't
read anything; we just return the result from the log.  Similarly,
when recording a "write" to the array, we record nothing (this write
operation has no result); so that when replaying, we redo nothing.

Note how that differs from anything managed by GC memory: GC objects
(including GC arrays) are really allocated, writes really occur, and
reads are redone.  We don't touch the log in this case.


Other reverse debuggers for Python
----------------------------------

There are already some Python experiments about `reverse debugging`_.
This is also known as "omniscient debugging".  However, I claim that
the result they get to is not very useful (for the purpose presented
here).  How they work is typically by recording changes to some
objects, like lists and dictionaries, in addition to recording the
history of where your program passed through.  However, the problem of
Python is that lists and dictionaries are not the end of the story.
There are many, many, many types of objects written in C which are
mutable---in fact, the immutable ones are the exception.  You can try
to systematically record all changes, but it is a huge task and easy
to forget a detail.

In other words it is a typical use case for tweaking the RPython
translation toolchain, rather than tweaking the CPython (or PyPy)
interpreter directly.  The result that we get here with RevPDB is more
similar to `rr`_ anyway, in that only a relatively small number of
external events are recorded---not every single change to every single
list and dictionary.

Some links:

* epdb: https://github.com/native-human/epdb

* pode: https://github.com/rodsenra/pode

For C:

* rr: http://rr-project.org/

* undodb-gdb: http://undo.io/

.. _`reverse debugging`: https://en.wikipedia.org/wiki/Debugger#Reverse_debugging
.. _`undodb-gdb`: http://undo.io/
.. _`rr`: http://rr-project.org/


Future work
-----------

As mentioned above, it is alpha-level, and only works on Linux with ASLR
disabled.  So the plans for the immediate future are to fix the various
issues described above, and port to more operating systems and remove
the restriction that requires a non-ASLR system.  The core of the system
is in the C file and headers in ``rpython/translator/revdb/src-revdb``.

For interested people, there is also the Duhton_ interpreter and its
``reverse-debugger`` branch, which is where I prototyped the RPython
concept before moving to PyPy.  The basics should work for any
interpreter written in RPython, but they require some specific code to
interface with the language; in the case of PyPy, it is in
``pypy/interpreter/reverse_debugging.py``.

.. _Duhton: https://bitbucket.org/pypy/duhton/

In parallel, there are various user interface improvements that people
could be interested in, like a more "pdb++" experience.  (And the script
at ``rpython/translator/revdb/revdb.py`` should be moved out into some
more "official" place, and the ``reverse-debugger`` branch should be
merged back to default.)

I would certainly welcome any help!

-+- Armin
