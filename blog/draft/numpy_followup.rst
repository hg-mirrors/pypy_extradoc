NumPy Follow Up
===============

Hi everyone.  Since yesterday's blog post we got a ton of feedback, so we want
to clarify a few things, as well as share some of the progress we've made, in
only the 24 hours since the post.

Reusing the original NumPy
--------------------------

First, a lot of people asked why we cannot just reuse the original NumPy
through ``cpyext``, our CPython C-API compatibility layer.  We believe this is
not the best approach, for a few reasons:

 1) ``cpyext`` is slow, and always will be slow. It has to emulate far too many
    details of the CPython object model that don't exist on PyPy (e.g.,
    reference counting). Since people are using NumPy primarily for speed this
    would mean that even if we could have a working NumPy, no one would want to
    use it.  Also, as soon as the execution crosses the ``cpyext`` boundary, it
    becomes invisible to the JIT.

 2) NumPy uses many obscure documented and undocumented details of the CPython
    C-API. Emulating these is often difficult or impossible (e.g. we can't fix
    accessing a struct field, as there's no function call for us to intercept).

 3) It's not much fun. Frankly, working on ``cpyext``, debugging the crashes,
    and everything else that goes with it is not terribly fun, especially when
    you know that the end result will be slow. We've demonstrated we can build
    a much faster NumPy, in a way that's more fun, and given the people working
    on this our volunteers, that's important to keep us motivated.

C bindings vs. CPython C-API
----------------------------

There are two issues on C code, one has a very nice story, and the other not so
much. First is the case of arbitrary C-code that isn't Python related, things
like ``libsqlite``, ``libbz2``, or any random C shared library on your system.
PyPy will quite happily call into these, and bindings can be developed either
at the RPython level (using ``rffi``) or in pure Python, using ``ctypes``.
Writing bindings with ``ctypes`` has the advantage that they can run on every
alternative Python implementation, such as Jython and IronPython.  Moreover,
once we merge the ``jittypes2`` branch ``ctypes`` calls will even be smoking
fast.

On the other hand there is the CPython C-extension API. This is a very specific
API which CPython exposes, and PyPy tries to emulate. It will never be fast,
because there is far too much overhead in all the emulation that needs to be
done.

One of the reasons people write C extension is speed.  Often, with PyPy you can
just forget about C, write everything in pure python and let the JIT to do its
magic.

In case the PyPy JIT alone isn't fast enough then it might make sense to split
your C-extension into 2 parts, one which doesn't touch the CPython C-API and
thus can be loaded with ``ctypes`` and called from PyPy, and another which does
the interfacing with Python for CPython (where it will be faster).

There are also libraries written in C to interface with existing C codebases,
but for whom performance is not the largest goal, for these the right solution
is to try using CPyExt, and if it works that's great, but if it fails the
solution will be to rewrite using `ctypes`, where it will work on all Python
VMs, not just CPython.


And finally there are rare cases where rewriting in RPython makes more sense,
NumPy is one of the few examples of these because we need to be able to give
the JIT hints on how to appropriately vectorize all of the operations on an
array.

Progress
--------

On a more positive note, after we published the `last post`_, several new people
came and contributed improvements to the numpy-exp branch.
We would like to thank all of them:

 * nightless_night contributed: An implementation of `__len__`, fixed bounds
   checks on `__getitem__` and `__setitem__`.
 * brentp contributed: Subtraction and division on NumPy arrays.
 * MostAwesomeDude contributed: Multiplication on NumPy arrays.
 * hodgestar contributed: Binary operations between floats and NumPy arrays.

Those last two were technically an outstanding branch we finally merged, but
hopefully you get the picture. In addition there was some exciting work done by
regular PyPy contributors. I hope it's clear that there's a place to jump in
for people with any level of PyPy familiarity. If you're interested in
contributing please stop by #pypy on irc.freenode.net, the
`pypy-dev <http://codespeak.net/mailman/listinfo/pypy-dev>`_ mailing list, or
send us pull requests on `bitbucket <https://bitbucket.org/pypy/pypy>`_.

Alex
