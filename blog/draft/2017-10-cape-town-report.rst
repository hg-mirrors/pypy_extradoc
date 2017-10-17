(Cape of) Good Hope for PyPy
----------------------------

Hello from the other side of the world (for most of you)!

With the excuse of coming to `PyCon ZA`_ during the last two weeks Armin,
Ronan, Antonio and sometimes Maciek had a very nice and productive sprint in
Cape Town, as pictures show :). We would like to say a big thank you to
Kiwi.com, which sponsored part of the travel costs via its awesome Sourcelift_
program to help Open Source projects.

.. _`PyCon ZA`: https://za.pycon.org/
.. _Sourcelift: https://www.kiwi.com/sourcelift/

XXX insert pic

Armin, Ronan and Anto spent most of the time hacking at cpyext, our CPython
C-API compatibility layer: during the last years, the focus was to make it
working and compatible with CPython, in order to run existing libraries such
as numpy and pandas. However, we never paid too much attention to performance,
so the net result is that with the latest released version of PyPy, C
extensions generally work but their speed ranges from "slow" to "horribly
slow".

For example, these very simple microbenchmarks_ measure the speed of
calling (empty) C functions, i.e. the time you spend to "cross the border"
between RPython and C. These are the results on CPython, on PyPy 5.9, and on
our newest in-progress version::

    $ python bench.py     # CPython
    noargs : 0.51 secs
    onearg : 0.45 secs
    varargs: 0.60 secs

    $ pypy-5.8 bench.py   # PyPy 5.8
    noargs : 1.11 secs
    onearg : 1.83 secs
    varargs: 3.50 secs

    $ pypy bench.py       # cpyext-refactor-methodobject branch
    noargs : 0.31 secs
    onearg : 0.37 secs
    varargs: 0.49 secs


.. _microbenchmarks: https://github.com/antocuni/cpyext-benchmarks
  
So yes: before the sprint, we were ~2-6x slower than CPython. Now, we are
**faster** than it!

To reach this result, we did various improvements, such as:

  1. teach the JIT how to look (a bit) inside the cpyext module

  2. write specialized code for calling ``METH_NOARGS``, ``METH_O`` and
     ``METH_VARARGS`` functions; previously, we always used a very general and
     slow logic;

  3. we implemented freelists to allocate the cpyext versions of ``int`` and
     ``tuple`` objects, as CPython does.
     
  4. the `cpyext-avoid-roundtrip`_ branch: crossing the RPython/C border is
     slowish, but the real problem was (and still is for many cases) we often
     cross it many times for no good reason. So, depending on the actual API
     call, you might end up in the C land, which calls back into the RPython
     land, which goes to C, etc. etc. (ad libitum).

The branch tries to fix such nonsense: so far, we fixed only some cases, which
are enough to speed up the benchmarks shown above.  But most importantly, we
now have a clear path and an actual plan to improve cpyext more and
more. Ideally, we would like to reach a point in which cpyext-intensive
programs run at worst at the same speed of CPython.

Among the other things, Armin and Maciej did a lot of work on the
`unicode-utf8`_ branch: the goal of the branch is to always use UTF-8 as the
internal representation of unicode strings. The advantages are various:

  - decoding an UTF-8 stream is super fast, as you just need to check that the
    stream is valid;

  - encoding to UTF-8 is a no-op;

  - in most cases, UTF-8 is a more compact representation than the currently
    used UCS-4.

Before you ask: yes, this branch contains special logic to ensure that random
access of single unicode chars is still O(1), as it is on both CPython and the
current PyPy.

In summary, this was a long and profitable sprint, in which we achieved lots
of interesting results. However, what we liked even more was the privilege of
doing commits_ from awesome places such as the top of Table Mountain:

.. _commits: https://bitbucket.org/pypy/pypy/commits/a4307fb5912e

XXX: embed this tweet
https://twitter.com/ronanlamy/status/915575026107240449
