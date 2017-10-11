(Cape of) Good Hope for PyPy
----------------------------

Hello from the other side of the world (for most of you)!

With the excuse of coming to PyCon ZA[1], during the last two weeks Armin,
Ronan, Antonio and Maciek had a very nice and productive sprint in Cape Town,
as pictures show :).

XXX insert pic

We spent most of the time hacking at cpyext, our CPython C-API compatibility
layer: during the last years, the focus was to make it working and compatible
with CPython, in order to run existing libraries such as numpy and
pandas. However, we never paid too much attention to performance, so the net
result is that with the latest released version of PyPy, C extensions
generally work but their speed ranges from "slow" to "horribly slow".

For example, these `very simple micro-benchmarks`_ measure the speed of
calling (empty) C functions, i.e. the time you spend to "cross the border"
between RPython and C. These are the results on CPython, on PyPy 5.9, and on
our newest in-progress version::
  
  bla bla bla


.. origin	git@github.com:antocuni/cpyext-benchmarks.git (fetch)

  
To reach this result, we did various improvements, such as:

  1. teach the JIT how to look (a bit) inside the cpyext module

  2. write specialized code for calling ``METH_NOARGS``, ``METH_O`` and
     ``METH_VARARGS`` functions; previously, we always used a very general and
     slow logic

  3. the `cpyext-avoid-roundtrip`_ branch: crossing the RPython/C border is
     slowish, but the real problem was (and still is for many cases) we often
     cross it many times for no good reason. So, depending on the actual API
     call, you might end up in the C land, which calls back into the RPython
     land, which goes to C, etc. etc. (ad libitum).

The branch tries to fix such nonsense: so far, we fixed only some cases, which
are enough to speed up the benchmarks shown above.  But most importantly, we
now have a clear path to improve cpyext more and more.

For example, the ``METH_VARARGS`` case is still a bit slowish because we need
to ``malloc()`` a new cpyext tuple for every call: the plan is to use the same
strategy as CPython, i.e. to use free lists to be able to quickly reuse the
memory as soon as the tuples die.

bla bla bla



