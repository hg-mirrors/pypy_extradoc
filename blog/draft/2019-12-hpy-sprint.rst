HPy kick-off sprint report
===========================

Recently Antonio, Armin and Ronan had a small internal sprint in the beautiful
city of Gdańsk to kick-off the development of HPy. Here is a brief report of
what was accomplished during the sprint.

What is HPy?
------------

The TL;DR answer is "a better way to write C extensions for Python".

The idea of HPy was born during EuroPython 2019 in Basel, where there was an
informal meeting which included core developers of PyPy, CPython (Victor
Stinner and Mark Shannon) and Cython (Stefan Behnel).

All of us agreed that the current design of the CPython C API is problematic
for various reasons and, in particular, because it is too tied to the current
internal design of CPython.  The end result is that:

  - alternative implementations of Python (such as PyPy, but not only) have a
    `hard time`_ loading and executing existing C extensions;

  - CPython itself is unable to change some of its internal implementation
    details without breaking the world. For example, as of today it would be
    impossible to switch from using reference counting to using a real GC,
    which in turns make it hard for example to remove the GIL, as gilectomy_
    attempted.

HPy tries to address these issues by following two major design guidelines:

  1. objects are referenced and passed around using opaque handles, which are
     similar to e.g., file descriptors in spirit. Multiple, different handles
     can point to the same underlying object, handles can be duplicated and
     each handle must be released independently of any other duplicate.

  2. The internal data structures and C-level layout of objects are not
     visible nor accessible using the API, so each implementation if free to
     use what fits best.

The other major design goal of HPy is to allow an incremental
transition/porting, so existing modules can migrate their codebase one method
at a time.  Moreover, Cython eventually will generate HPy code, so extension
module written in Cython will be able to benefit from HPy automatically.

More details can be found in the README of the official `HPy repository`_.

.. _`hard time`: https://morepypy.blogspot.com/2018/09/inside-cpyext-why-emulating-cpython-c.html
.. _gilectomy: https://pythoncapi.readthedocs.io/gilectomy.html
.. _`HPy repository`: https://github.com/pyhandle/hpy


CPython and universal target ABI
---------------------------------

When compiling an HPy extension you can choose two different target ABIs:

  - **CPython ABI**: in this case, ``hpy.h`` contains a set of macros and
    static inline functions which at compilation time translates the HPy API
    into the standard C-API: the compiled module will have no performance
    penalty and it will have an filename like
    ``foo.cpython-37m-x86_64-linux-gnu.so``.

  - **Universal HPy ABI**: as the name implies, extension modules compiled
    this way are "universal" and can be loaded unmodified by multiple Python
    interpreters and version.  Moreover, it will be possible to dynamically
    enable a special debug mode which will make it easy to find e.g., open
    handles or memory leaks, **without having to recompile the extension**.


Universal modules can be loaded **also** on CPython, thanks to the
``hpy_universal`` module which is under development. An extra layer of
indirection enables loading extensions compiled with the universal ABI. Users
of ``hpy_universal`` will face a small performance penalty compared to the ones
using the CPython ABI mode.

This setup gives several benefits:

  - extension developers can use the extra debug features given by the
    Universal ABI with no need to use a special debug version of Python

  - projects which need the maximum level of performance can compile their
    extension for each relevant version of CPython, as they are doing now

  - projects for which runtime speed is less important will have the choice of
    distributing a single binary which will work on any version and
    implementation of Python


A simple example
-----------------

The HPy repo contains a `proof of concept`_ module. Here is a simplified
version which illustrates what a HPy module looks like:

.. sourcecode:: C

    #include "hpy.h"

    HPy_DEF_METH_VARARGS(add_ints)
    static HPy add_ints_impl(HPyContext ctx, HPy self, HPy *args, HPy_ssize_t nargs)
    {
        long a, b;
        if (!HPyArg_Parse(ctx, args, nargs, "ll", &a, &b))
            return HPy_NULL;
        return HPyLong_FromLong(ctx, a+b);
    }


    static HPyMethodDef PofMethods[] = {
        {"add_ints", add_ints, HPy_METH_VARARGS, ""},
        {NULL, NULL, 0, NULL}
    };

    static HPyModuleDef moduledef = {
        HPyModuleDef_HEAD_INIT,
        .m_name = "pof",
        .m_doc = "HPy Proof of Concept",
        .m_size = -1,
        .m_methods = PofMethods
    };


    HPy_MODINIT(pof)
    static HPy init_pof_impl(HPyContext ctx)
    {
        HPy m;
        m = HPyModule_Create(ctx, &moduledef);
        if (HPy_IsNull(m))
            return HPy_NULL;
        return m;
    }


People who are familiar with the current C-API will surely notice lots of
similarities. The biggest differences are:

  - Instead of ``PyObject *``, objects have the type ``HPy``, which as
    explained above represents a handle.

  - You need to explicitly pass an ``HPyContext`` around: the intent is
    primary to be future-proof and make it easier to implement things like
    sub- interpreters.

  - ``HPy_METH_VARARGS`` is implemented differently than CPython's
    ``METH_VARARGS``: in particular, these methods receive an array of ``HPy``
    and its length, instead of a fully constructed tuple: passing a tuple
    makes sense on CPython where you have it anyway, but it might be an
    unnecessary burden for alternate implementations.  Note that this is
    similar to the new `METH_FASTCALL` which was introduced in CPython.

  - HPy relies a lot on C macros, which most of the time are needed to support
    the CPython ABI compilation mode. For example, ``HPy_DEF_METH_VARARGS``
    expands into a trampoline which has the correct C signature that CPython
    expects (i.e., ``PyObject (*)(PyObject *self, *PyObject *args)``) and
    which calls ``add_ints_impl``.


.. _`proof of concept`: https://github.com/pyhandle/hpy/blob/master/proof-of-concept/pof.c
.. _`METH_FASTCALL`: https://www.python.org/dev/peps/pep-0580/


Sprint report and current status
---------------------------------

XXX finish me
