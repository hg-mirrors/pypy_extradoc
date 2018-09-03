Inside cpyext: why emulating CPython C API is so hard
======================================================

cpyext is PyPy's subsistem which is responsible to provide a compatibility
layer to compile and run CPython C extensions inside PyPy.  Often people asks
why a particular extension doesn't work or it is very slow on PyPy, but
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

At the C level, Python objects are represented as ``PyObject *``,
i.e. (mostly) opaque pointers to some common "base struct".

CPython uses a very simple memory management scheme: when you create an
object, you allocate a block of memory of the appropriate size on the heap:
depending on the details you might end up calling different allocators, but
for the sake of simplicity, you can think that this ends up being a call to
``malloc()``. The resulting block of memory is initialized and casted to to
``PyObject *``: this address never changes during the object lifetime, and the
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

Generally speaking, the only way to operate on ``PyObject *`` is to call the
appropriate API functions. For example, to convert a given object as a C
integer, you can use _`PyInt_AsLong()`; to add to objects together, you can
call _`PyNumber_Add()`

.. _`PyInt_AsLong()`: https://docs.python.org/2/c-api/int.html?highlight=pyint_check#c.PyInt_AsLong
.. _`PyNumber_Add()`: https://docs.python.org/2/c-api/number.html#c.PyNumber_Add

Internally, PyPy uses a similar approach: all Python objects are subclasses of
the RPython ``W_Root`` class, and they are operated by calling methods on the
``space`` singleton, which represents the interpreter.

At first, it looks very easy to write a compatibility layer: just make
``PyObject *`` an alias for ``W_Root``, and write simple RPython functions
(which will be translated to C by the RPython compiler) which call the
``space`` accordingly:

.. sourcecode:: python

   def PyInt_AsLong(space, o):
       return space.int_w(o)

   def PyNumber_Add(space, o1, o2):
       return space.add(o1, o2)


Actually, the code above is not too far from the actual
implementation. However, there are tons of gory details which makes it much
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
hand, we need a way to represent them as fixed-address ``PyObject *`` when we
pass them to C extensions.  We surely need a way to handle that.
