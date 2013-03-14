PyPy without the GIL
====================

Description
-----------

PyPy has a version without the Global Interpreter Lock (GIL). It can run
multiple threads concurrently. But the real benefit is that you have
other, new ways of using all your cores. In this talk I will describe
how it is possible (STM) and then focus on some of these new
opportunities, e.g. show how we used multiple cores in a single really
big program without adding thread locks everywhere.

Abstract
--------

PyPy has a version without the Global Interpreter Lock (GIL). It can run
multiple threads concurrently. Internally, this is possible thanks to
Software Transactional Memory (STM). But the real benefit is that STM
gives other, new ways of using all your cores.

In this talk I will describe the basics of STM which make it possible,
and give a word about the upcoming Hardware Transactional Memory. I will
then focus on some of these new opportunities. Indeed, PyPy can run a
single multi-threaded program using multiple cores --- but using threads
in the first place is a brittle endeavour, even in Python (even if not
as much as in lower-level languages). You have to carefully use implicit
or explicit locking, at one level or another, and in a large program,
each missing lock equals to one rare non-reproducible bug.

With STM, other options arise naturally if you can control the length of
each "transaction". I will show a small library that uses threads
internally, but in which each thread executes a series of (large)
transactions. This gives a very clean high-level view that seems to have
no concurrency at all, while internally running transactions in
parallel.

Obviously this is not a silver bullet: usually, you still have to work
on debugging your program. But the program is always correct, and you
fight efficiency bugs --- as opposed to the regular multi-threaded
model, where the program is always efficient, but you fight correctness
bugs.
