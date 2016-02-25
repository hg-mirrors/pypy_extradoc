CAPI Support update
===================

As you know, PyPy can emulate the CPython C API to some extent.  It is
done by passing around ``PyObject *`` pointers.  Inside PyPy, the
objects don't have the same ``PyObject *`` structure at all; and
additionally their memory address can change.  PyPy handles the
difference by maintaining two sets of objects.  More precisely, starting
from a PyPy object, it can allocate on demand a ``PyObject`` structure
and fill it with information that points back to the original PyPy
objects; and conversely, starting from a C-level object, it can allocate
a PyPy-level object and fill it with information in the opposite
direction.

I have merged a rewrite of the interaction between C-API C-level objects
and PyPy's interpreter level objects.  This is mostly a simplification
based on a small hack in our garbage collector.  This hack makes the
garbage collector aware of the reference-counted ``PyObject``
structures.  When it considers a pair consisting of a PyPy object and a
``PyObject``, it will always free either none or both of them at the
same time.  They both stay alive if *either* there is a regular GC
reference to the PyPy object, *or* the reference counter in the
``PyObject`` is bigger than zero.

This gives a more stable result.  Previously, a PyPy object might grow a
corresponding ``PyObject``, loose it (when its reference counter goes to
zero), and later have another corresponding ``PyObject`` re-created at a
different address.  Now, once a link is created, it remains alive until
both objects die.

The rewrite significantly simplifies our previous code (which used to be
based on at least 4 different dictionaries), and should make using the
C-API less slow (it is still slower than using pure python or cffi).

So, the good news is that now PyPy actually supports the upstream
`lxml`_ package---which is is one of the most popular packages on PyPI.
(Specifically, you need version 3.5.0 with
https://github.com/lxml/lxml/pull/187 to remove old PyPy-specific hacks
that were not really working.)  At this point, we no longer recommend
using the `cffi lxml`_ alternative: although it may still be faster, it
might be incomplete and old.

We are actively working on extending our C-API support, and hope to soon
merge a branch to support more of the C-API functions (some numpy news
coming!).  Please `try it out`_ and let us know how it works for you.

_`lxml`: https://github.com/lxml/lxml
_`try it out`: http://buildbot.pypy.org/nightly/trunk/

Armin Rigo and the PyPy team
