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


``PyObject*`` in PyPy
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
we are in the PyPy world (the movable ``W_Root`` subclass) or in the C world
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
C land, we store the current thread id into a global variable which is
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

Prior to the `2017 Cape Town Sprint`_, cpyext was horribly slow, and we were
well aware of it: the main reason was that we never really paid too much
attention to performances: as explained by this blog post, emulating all the
CPython quirks is basically a nightmare, so better to concentrate on
correctness first.

However, we didn't really know **why** it was so slow: we had theories and
assumptions, usually pointing at the cost of conversions between ``W_Root``
and ``PyObject*``, but we never actually measured it.

So, I decided to write a set of `cpyext microbenchmarks`_ to measure the
performance of various operation.  The result was somewhat surprising: the
theory suggests that when you do a cpyext C call, you should pay the
border-crossing costs only once, but what the profiler told us was that we
were paying the cost of ``generic_cpy_call`` several times what we expected.

After a bit of investigation, we discovered this was ultimately caused by our
"correctness-first" approach.  For simplicity of development and testing, when
we started cpyext we wrote everything in RPython: thus, every single API call
made from C (like the omnipresent `PyArg_ParseTuple`_, `PyInt_AsLong`_, etc.)
had to cross back the C-to-RPython border: this was especially daunting for
very simple and frequent operations like ``Py_INCREF`` and ``Py_DECREF``,
which CPython implements as a single assembly instruction!

Another source of slowness was the implementation of ``PyTypeObject`` slots:
at the C level, these are function pointers which the interpreter calls to do
certain operations, e.g. `tp_new`_ to allocate a new instance of that type.

As usual, we have some magic to implement slots in RPython; in particular,
`_make_wrapper`_ does the opposite of ``generic_cpy_call``: it takes an
RPython function and wraps it into a C function which can be safely called
from C, handling the GIL, exceptions and argument conversions automatically.

This was very handy during the development of cpyext, but it might result in
some bad nonsense; consider what happens when you call the following C
function:

.. sourcecode:: C

    static PyObject* foo(PyObject* self, PyObject* args)
    {
        PyObject* result = PyInt_FromLong(1234);
        return result;
    }

  1. you are in RPython and do a cpyext call to ``foo``: **RPython-to-C**;

  2. ``foo`` calls ``PyInt_FromLong(1234)``, which is implemented in RPython:
     **C-to-RPython**;

  3. the implementation of ``PyInt_FromLong`` indirectly calls
     ``PyIntType.tp_new``, which is a C function pointer: **RPython-to-C**;

  4. however, ``tp_new`` is just a wrapper around an RPython function, created
     by ``_make_wrapper``: **C-to-RPython**;

  5. finally, we create our RPython ``W_IntObject(1234)``; at some point
     during the **RPython-to-C** crossing, its ``PyObject*`` equivalent is
     created;

  6. after many layers of wrappers, we are again in ``foo``: after we do
     ``return result``, during the **C-to-RPython** step we convert it from
     ``PyObject*`` to ``W_IntObject(1234)``.

Phew! After we realized this, it was not so surprising that cpyext was very
slow :). And this was a simplified example, since we are not passing and
``PyObject*`` to the API call: if we did, we would need to convert it back and
forth at every step.  Actually, I am not even sure that what I described was
the exact sequence of steps which used to happen, but you get the general
idea.

The solution is simple: rewrite as much as we can in C instead of RPython, so
to avoid unnecessary roundtrips: this was the topic of most of the Cape Town
sprint and resulted in the ``cpyext-avoid-roundtrip`` branch, which was
eventually merged_.

Of course, it is not possible to move **everything** to C: there are still
operations which need to be implemented in RPython. For example, think of
``PyList_Append``: the logic to append an item to a list is complex and
involves list strategies, so we cannot replicate it in C.  However, we
discovered that a large subset of the C API can benefit from this.

Moreover, the C API is **huge**: the biggest achievement of the branch was to
discover and invent this new way of writing cpyext code, but we still need to
convert many of the functions.  Also, sometimes the rewrite is not automatic
or straighforward: cpyext is a delicate piece of software, so it happens often
that you end up debugging a segfault in gdb.

However, the most important remark is that the performance improvement we got
from this optimization are impressive, as we will detail later.

.. _`2017 Cape Town Sprint`: https://morepypy.blogspot.com/2017/10/cape-of-good-hope-for-pypy-hello-from.html
.. _`cpyext microbenchmarks`: https://github.com/antocuni/cpyext-benchmarks
.. _`PyArg_ParseTuple`: https://docs.python.org/2/c-api/arg.html#c.PyArg_ParseTuple
.. _`PyInt_AsLong`: https://docs.python.org/2/c-api/int.html#c.PyInt_AsLong
.. _`tp_new`: https://docs.python.org/2/c-api/typeobj.html#c.PyTypeObject.tp_new
.. `_make_wrapper`: https://bitbucket.org/pypy/pypy/src/b9bbd6c0933349cbdbfe2b884a68a16ad16c3a8a/pypy/module/cpyext/api.py#lines-362
.. _merged: https://bitbucket.org/pypy/pypy/commits/7b550e9b3cee   


Conversion costs
-----------------

The other potential big source of slowdown is the conversion of arguments
between ``W_Root`` and ``PyObject*``.

As explained earlier, the first time you pass a ``W_Root`` to C, you need to
allocate it's ``PyObject*`` counterpart. Suppose to have a ``foo`` function
defined in C, which takes a single int argument:

.. sourcecode:: python

   for i in range(N):
       foo(i)

To run this code, you need to create a different ``PyObject*`` for each value
of ``i``: if implemented naively, it means calling ``N`` times ``malloc()``
and ``free()``, which kills performance.

CPython has the very same problem, which is solved by using a `free list`_ to
`allocate ints`_. So, what we did was to simply `steal the code`_ from CPython
and do the exact same thing: this was also done in the
``cpyext-avoid-roundtrip`` branch, and the benchmarks show that it worked
perfectly.

Every type which is converted often to ``PyObject*`` must have a very fast
allocator: at the moment of writing, PyPy uses free lists only for ints and
tuples_: one of the next steps on our TODO list is certainly to use this
technique with more types, like ``float``.

Conversely, we also need to optimize the converstion from ``PyObject*`` to
``W_Root``: this happens when an object is originally allocated in C and
returned to Python. Consider for example the following code:

.. sourcecode:: python

   import numpy as np
   myarray = np.random.random(N)
   for i in range(len(arr)):
       myarray[i]

At every iteration, we get an item out of the array: the return type is a an
instance of ``numpy.float64`` (a numpy scalar), i.e. a ``PyObject'*``: this is
something which is implemented by numpy entirely in C, so completely
transparent to cpyext: we don't have any control on how it is allocated,
managed, etc., and we can assume that allocation costs are the same than on
CPython.

As soon as we return these ``PyObject*`` to Python, we need to allocate
theirs ``W_Root`` equivalent: if you do it in a small loop like in the example
above, you end up allocating all these ``W_Root`` inside the nursery, which is
a good thing since allocation is super fast (see the section above about the
PyPy GC).

However, we also need to keep track of the ``W_Root`` to ``PyObject*`` link:
currently, we do this by putting all of them in a dictionary, but it is very
inefficient, especially because most of these objects dies young and thus it
is wasted work to do that for them.  Currently, this is one of the biggest
unresolved problem in cpyext, and it is what casuses the two microbenchmarks
``allocate_int`` and ``allocate_tuple`` to be very slow.

We are well aware of the problem, and we have a plan for how to fix it; the
explanation is too technical for the scope of this blog post as it requires a
deep knowledge of the GC internals to be understood, but the details are
here_.

.. _`free list`: https://en.wikipedia.org/wiki/Free_list
.. _`allocate ints`: https://github.com/python/cpython/blob/2.7/Objects/intobject.c#L16
.. _`steal the code`: https://bitbucket.org/pypy/pypy/commits/e5c7b7f85187
.. _tuples: https://bitbucket.org/pypy/pypy/commits/ccf12107e805
.. _here: https://bitbucket.org/pypy/extradoc/src/cd51a2e3fc4dac278074997c7dc198caee819769/planning/cpyext.txt#lines-27


C API quirks
--------------------

Finally, there is another source of slowdown which is beyond our control: some
parts of the CPython C API are badly designed and expose some of the
implementation details of CPython.

The major example is reference counting: the ``Py_INCREF`` / ``Py_DECREF`` API
is designed in such a way which forces other implementation to emulate
refcounting even in presence of other GC management schemes, as explained
above.

Another example is borrowed references: there are API functions which **do
not** incref an object before returning it, e.g. `PyList_GetItem`_.  This is
done for performance reasons because we can avoid a whole incref/decref pair,
if the caller needs to handle the returned item only temporarily: the item is
kept alive because it is in the list anyway.

For PyPy this is a challenge: thanks to `list strategies`_, often lists are
represented in a compact way: e.g. a list containing only integers is stored
as a C array of ``long``.  How to implement ``PyList_GetItem``? We cannot
simply create a ``PyObject*`` on the fly, because the caller will never decref
it and it will result in a memory leak.

The current solution is very inefficient: basically, the first time we do a
``PyList_GetItem``, we convert_ the **whole** list to a list of
``PyObject*``. This is bad in two ways: the first is that we potentially pay a
lot of unneeded conversion cost in case we will never access the other items
of the list; the second is that by doing that we lose all the performance
benefit granted by the original list strategy, making it slower even for the
rest of pure-python code which will manipulate the list later.

``PyList_GetItem`` is an example of a bad API because it assumes that the list
is implemented as an array of ``PyObject*``: after all, in order to return a
borrowed reference, we need a reference to borrow, don't we?

Fortunately, (some) CPython developers are aware of these problems, and there
is an ongoing project to `design a better C API`_ which aims to fix exactly
this kind of problems.

Nonetheless, in the meantime we still need to implement the current
half-broken APIs: there is no easy solutions for that, and it is likely that
we will always need to pay some performance penalty in order to implement them
correctly.

However, what we could potentially do is to provide alternative functions
which do the same job but are more PyPy friendly: for example, we could think
of implementing ``PyList_GetItemNonBorrowed`` or something like that: then, C
extensions could choose to use it (possibly hidden inside some macro and
``#ifdef``) if they want to be fast on PyPy.


.. _`PyList_GetItem`: https://docs.python.org/2/c-api/list.html#c.PyList_GetItem
.. _`list strategies`: https://morepypy.blogspot.com/2011/10/more-compact-lists-with-list-strategies.html
.. _convert: https://bitbucket.org/pypy/pypy/src/b9bbd6c0933349cbdbfe2b884a68a16ad16c3a8a/pypy/module/cpyext/listobject.py#lines-28
.. _`design a better C API`: https://pythoncapi.readthedocs.io/
