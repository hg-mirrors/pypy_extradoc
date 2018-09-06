Inside cpyext: why emulating CPython C API is so hard
======================================================

cpyext is PyPy's subsistem which is responsible to provide a compatibility
layer to compile and run CPython C extensions inside PyPy.  Often people asks
why it this particular extension doesn't work or it is very slow on PyPy, but
usually it is hard to answer without going into technical details: the goal of
this blog post is to explain some of these technical details, so that we can
simply link here instead of explaing again and again :).

From a 10.000 foot view, cpyext is PyPy's version of ``"Python.h"``: every time
you compile and extension which uses that header file, you are using cpyext:
this includes extension explicitly written in C (such as ``numpy``) and
extensions which are generated from other compilers/preprocessors
(e.g. ``Cython``).

At the time of writing, the current status is that most C extensions "just
work": generally speaking, you can simply ``pip install`` all of them,
provided they use the public, `official C API`_ instead of poking at private
implementation details.  However, the performance of cpyext are generally
poor, meaning that a Python program which makes heavy use of cpyext extensions
is likely to be slower on PyPy than on CPython.

.. _`official C API`: https://docs.python.org/2/c-api/index.html


C API Overview
---------------

In CPython, at the C level, Python objects are represented as ``PyObject*``,
i.e. (mostly) opaque pointers to some common "base struct".

CPython uses a very simple memory management scheme: when you create an
object, you allocate a block of memory of the appropriate size on the heap;
depending on the details you might end up calling different allocators, but
for the sake of simplicity, you can think that this ends up being a call to
``malloc()``. The resulting block of memory is initialized and casted to to
``PyObject*``: this address never changes during the object lifetime, and the
C code can freely pass it around, store it inside containers, retrieve it
later, etc.

Memory is managed using reference counting: when you create a new reference to
an object, or you discard a reference you own, you have to increment_ or
decrement_ reference counter accordingly. When the reference counter goes to
0, it means that the object is no longer used by anyone and can safely be
destroyed. Again, we can simplify and say that this results in a call to
``free()``, which finally releases the memory which was allocated by ``malloc()``.

.. _increment: https://docs.python.org/2/c-api/refcounting.html#c.Py_INCREF
.. _decrement: https://docs.python.org/2/c-api/refcounting.html#c.Py_DECREF

Generally speaking, the only way to operate on ``PyObject*`` is to call the
appropriate API functions. For example, to convert a given ``PyObject*`` to a C
integer, you can use _`PyInt_AsLong()`; to add two objects together, you can
call _`PyNumber_Add()`.

.. _`PyInt_AsLong()`: https://docs.python.org/2/c-api/int.html?highlight=pyint_check#c.PyInt_AsLong
.. _`PyNumber_Add()`: https://docs.python.org/2/c-api/number.html#c.PyNumber_Add

Internally, PyPy uses a similar approach: all Python objects are subclasses of
the RPython ``W_Root`` class, and they are operated by calling methods on the
``space`` singleton, which represents the interpreter.

At first, it looks very easy to write a compatibility layer: just make
``PyObject*`` an alias for ``W_Root``, and write simple RPython functions
(which will be translated to C by the RPython compiler) which call the
``space`` accordingly:

.. sourcecode:: python

   def PyInt_AsLong(space, o):
       return space.int_w(o)

   def PyNumber_Add(space, o1, o2):
       return space.add(o1, o2)


Actually, the code above is not too far from the actual
implementation. However, there are tons of gory details which make it much
harder than what it looks, and much slower unless you pay a lot of attention
to performance.


The PyPy GC
-------------

To understand some of cpyext challenges, you need to have at least a rough
idea of how the PyPy GC works.

XXX: maybe the following section is too detailed and not really necessary to
understand cpyext? We could simplify it by saying "PyPy uses a generational
GC, objects can move".

Contrarily to the popular belief, the "Garbage Collector" is not only about
collecting garbage: instead, it is generally responsible of all memory
management, including allocation and deallocation.

Whereas CPython uses a combination of malloc/free/refcounting to manage
memory, the PyPy GC uses a completely different approach. It is designed
assuming that a dynamic language like Python behaves the following way:

  - you create, either directly or indirectly, lots of objects;

  - most of these objects are temporary and very short-lived: think e.g. of
    doing ``a + b + c``: you need to allocate an object to hold the temporary
    result of ``a + b``, but it dies very quickly because you no longer need it
    when you do the final ``+ c`` part;

  - only small fraction of the objects survives and stay around for a while.

So, the strategy is: make allocation as fast as possible; make deallocation of
short-lived objects as fast as possible; find a way to handle the remaining
small set of objects which actually survive long enough to be important.

This is done using a **Generational GC**: the basic idea is the following:

  1. we have a nursery, where we allocate "young objects" very fast;

  2. when the nursery is full, we start what we call a "minor collection": we
     do quick scan to determine the small set of objects which survived so
     far;

  3. we **move** these objects out of the nursery, and we place them in the
     area of memory which contains the "old objects"; since the address of the
     objects just changed, we fix all the references to them accordingly;

  4. now the nursery contains only objects which died young: we can simply
     discard all of them very quickly, reset the nursery and use the same area
     of memory to allocate new objects from now.

In practice, this scheme works very well and it is one of the reasons why PyPy
is much faster than CPython.  However, careful readers have surely noticed
that this is a problem for ``cpyext``: on one hand, we have PyPy objects which
can potentially move and change their underlying memory address; on the other
hand, we need a way to represent them as fixed-address ``PyObject*`` when we
pass them to C extensions.  We surely need a way to handle that.


`PyObject*` in PyPy
---------------------

Another challenge is that sometimes, ``PyObject*`` structs are not completely
opaque: there are parts of the public API which expose to the user specific
fields of some concrete C struct, for example the definition of PyTypeObject_:
since the low-level layout of PyPy ``W_Root`` objects is completely different
than the one used by CPython, we cannot simply pass RPython objects to C; we
need a way to handle the difference.

.. _PyTypeObject: https://docs.python.org/2/c-api/typeobj.html

So, we have two issues so far: objects which can move, and incompatible
low-level layouts. ``cpyext`` solves both by decoupling the RPython and the C
representations: we have two "views" of the same entity, depending on whether
we are in the PyPy world (the moving ``W_Root`` subclass) or in the C world
(the non-movable ``PyObject*``).

``PyObject*`` are created lazily, only when they are actually needed: the
vast majority of PyPy objects are never passed to any C extension, so we don't
pay any penalty in that case; however, the first time we pass a ``W_Root`` to
C, we allocate and initialize its ``PyObject*`` counterpart.

The same idea applies also to objects which are created in C, e.g. by calling
_`PyObject_New`: at first, only the ``PyObject*`` exists and it is
exclusively managed by reference counting: as soon as we pass it to the PyPy
world (e.g. as a return value of a function call), we create its ``W_Root``
counterpart, which is managed by the GC as usual.

.. _`PyObject_New`: https://docs.python.org/2/c-api/allocation.html#c.PyObject_New

Here we start to see why calling cpyext modules is more costly in PyPy than in
CPython: we need to pay some penalty for all the conversions between
``W_Root`` and ``PyObject*``.

Moreover, the first time we pass a ``W_Root`` to C we also need to allocate
the memory for the ``PyObject*`` using a slowish "CPython-style" memory
allocator: in practice, for all the objects which are passed to C we pay more
or less the same costs as CPython, thus effectively "undoing" the speedup
guaranteed by PyPy's Generational GC under normal circumstances.


Maintaining the link between ``W_Root`` and ``PyObject*``
-----------------------------------------------------------

So, we need a way to convert between ``W_Root`` and ``PyObject*`` and
vice-versa; also, we need to to ensure that the lifetime of the two entities
are in sync. In particular:

  1. as long as the ``W_Root`` is kept alive by the GC, we want the
     ``PyObject*`` to live even if its refcount drops to 0;

  2. as long as the ``PyObject*`` has a refcount greater than 0, we want to
     make sure that the GC does not collect the ``W_Root``.

The ``PyObject*`` ==> ``W_Root`` link is maintained by the special field
_`ob_pypy_link` which is added to all ``PyObject*``: on a 64 bit machine this
means that all ``PyObject*`` have 8 bytes of overhead, but then the
conversion is very quick, just reading the field.

For the other direction, we generally don't want to do the same: the
assumption is that the vast majority of ``W_Root`` objects will never be
passed to C, and adding an overhead of 8 bytes to all of them is a
waste. Instead, in the general case the link is maintained by using a
dictionary, where ``W_Root`` are the keys and ``PyObject*`` the values.

However, for a _`few selected` ``W_Root`` subclasses we **do** maintain a
direct link using the special ``_cpy_ref`` field to improve performance. In
particular, we use it for ``W_TypeObject`` (which is big anyway, so a 8 bytes
overhead is negligible) and ``W_NoneObject``: ``None`` is passed around very
often, so we want to ensure that the conversion to ``PyObject*`` is very
fast. Moreover it's a singleton, so the 8 bytes overhead is negligible as
well.

This means that in theory, passing an arbitrary Python object to C is
potentially costly, because it involves doing a dictionary lookup.  I assume
that this cost will eventually show up in the profiler: however, at the time
of writing there are other parts of cpyext which are even more costly (as we
will show later), so the cost of the dict lookup is never evident in the
profiler.


.. _`ob_pypy_link`: https://bitbucket.org/pypy/pypy/src/942ad6c1866e30d8094d1dae56a9b8f492554201/pypy/module/cpyext/parse/cpyext_object.h#lines-5

.. _`few selected`: https://bitbucket.org/pypy/pypy/src/942ad6c1866e30d8094d1dae56a9b8f492554201/pypy/module/cpyext/pyobject.py#lines-66


Crossing the border between RPython and C
------------------------------------------

There are two other things we need to care about whenever we cross the border
between RPython and C, and vice-versa: exception handling and the GIL.

In the C API, exceptions are raised by calling `PyErr_SetString()`_ (or one of
`many other functions`_ which have a similar effect), which basically works by
creating an exception value and storing it in some global variable; then, the
function signals that an exception has occurred by returning an error value,
usually ``NULL``.

On the other hand, in the PyPy interpreter they are propagated by raising the
RPython-level OperationError_ exception, which wraps the actual app-level
exception values: to harmonize the two worlds, whenever we return from C to
RPython, we need to check whether a C API exception was raised and turn it
into an ``OperationError`` if needed.

About the GIL, we won't dig into details of `how it is handled in cpyext`_:
for the purpose of this post, it is enough to know that whenever we enter the
C land, we store the current theead id into a global variable which is
accessible also from C; conversely, whenever we go back from RPython to C, we
restore this value to 0.

Similarly, we need to do the inverse operations whenever you need to cross the
border between C and RPython, e.g. by calling a Python callback from C code.

All this complexity is automatically handled by the RPython function
`generic_cpy_call`_: if you look at the code you see that it takes care of 4
things:

  1. handling the GIL as explained above

  2. handling exceptions, if they are raised

  3. converting arguments from ``W_Root`` to ``PyObject*``

  4. converting the return value from ``PyObject*`` to ``W_Root``


So, we can see that calling C from RPython introduce some overhead: how much
is it?

Assuming that the conversion between ``W_Root`` and ``PyObject*`` has a
reasonable cost (as explained by the previous section), the overhead
introduced by a single border-cross is still accettable, especially if the
callee is doing some non-negligible amount of work.

However this is not always the case; there are basically three problems that
make (or used to make) cpyext super slow:

  1. paying the border-crossing cost for trivial operations which are called
     very often, such as ``Py_INCREF``

  2. crossing the border back and forth many times, even if it's not strictly
     needed

  3. paying an excessive cost for argument and return value conversions


The next sections are going to explain in more detail each of these problems.

.. _`PyErr_SetString()`: https://docs.python.org/2/c-api/exceptions.html#c.PyErr_SetString
.. _`many other functions`: https://docs.python.org/2/c-api/exceptions.html#exception-handling
.. _OperationError: https://bitbucket.org/pypy/pypy/src/b9bbd6c0933349cbdbfe2b884a68a16ad16c3a8a/pypy/interpreter/error.py#lines-20
.. _`how it is handled in cpyext`: https://bitbucket.org/pypy/pypy/src/b9bbd6c0933349cbdbfe2b884a68a16ad16c3a8a/pypy/module/cpyext/api.py#lines-205
.. _`generic_cpy_call`: https://bitbucket.org/pypy/pypy/src/b9bbd6c0933349cbdbfe2b884a68a16ad16c3a8a/pypy/module/cpyext/api.py#lines-1757


Avoiding unnecessary roundtrips
--------------------------------

XXX basically, this section explains what we did in the cpyext-avoid-roundtrips branch, and what we still need to do


Conversion costs
-----------------

XXX this is one of the biggest unsolved problems so far; explain or link to
this:

https://bitbucket.org/pypy/extradoc/src/cd51a2e3fc4dac278074997c7dc198caee819769/planning/cpyext.txt#lines-27


Borrowed references
--------------------

XXX explain why borrowed references are a problem for us; possibly link to: https://pythoncapi.readthedocs.io/bad_api.html#borrowed-references
