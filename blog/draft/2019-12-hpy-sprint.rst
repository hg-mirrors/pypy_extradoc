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
Stinner and Mark Shannon) and Cython (Stefan Behnel). The ideas were later also
discussed with Tim Felgentreff of GraalPython_, to make sure they would also be
applicable to this very different implementation, Windel Bouwman of RustPython_
is following the project as well.

.. _GraalPython: https://github.com/graalvm/graalpython
.. _RustPython: https://github.com/RustPython/RustPython

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

The other major design goal of HPy is to allow incremental transition and
porting, so existing modules can migrate their codebase one method at a time.
Moreover, Cython is considering to optionally generate HPy code, so extension
module written in Cython would be able to benefit from HPy automatically.

More details can be found in the README of the official `HPy repository`_.

.. _`hard time`: https://morepypy.blogspot.com/2018/09/inside-cpyext-why-emulating-cpython-c.html
.. _gilectomy: https://pythoncapi.readthedocs.io/gilectomy.html
.. _`HPy repository`: https://github.com/pyhandle/hpy


Target ABI
-----------

When compiling an HPy extension you can choose one of two different target ABIs:

  - **HPy/CPython ABI**: in this case, ``hpy.h`` contains a set of macros and
    static inline functions. At compilation time this translates the HPy API
    into the standard C-API. The compiled module will have no performance
    penalty, and it will have a "standard" filename like
    ``foo.cpython-37m-x86_64-linux-gnu.so``.

  - **Universal HPy ABI**: as the name implies, extension modules compiled
    this way are "universal" and can be loaded unmodified by multiple Python
    interpreters and versions.  Moreover, it will be possible to dynamically
    enable a special debug mode which will make it easy to find e.g., open
    handles or memory leaks, **without having to recompile the extension**.


Universal modules can **also** be loaded on CPython, thanks to the
``hpy_universal`` module which is under development. An extra layer of
indirection enables loading extensions compiled with the universal ABI. Users
of ``hpy_universal`` will face a small performance penalty compared to the ones
using the HPy/CPython ABI.

This setup gives several benefits:

  - Extension developers can use the extra debug features given by the
    Universal ABI with no need to use a special debug version of Python.

  - Projects which need the maximum level of performance can compile their
    extension for each relevant version of CPython, as they are doing now.

  - Projects for which runtime speed is less important will have the choice of
    distributing a single binary which will work on any version and
    implementation of Python.


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


People who are familiar with the current C-API will surely notice many
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
    similar to the new `METH_FASTCALL`_ which was introduced in CPython.

  - HPy relies a lot on C macros, which most of the time are needed to support
    the HPy/CPython ABI compilation mode. For example, ``HPy_DEF_METH_VARARGS``
    expands into a trampoline which has the correct C signature that CPython
    expects (i.e., ``PyObject (*)(PyObject *self, *PyObject *args)``) and
    which calls ``add_ints_impl``.


.. _`proof of concept`: https://github.com/pyhandle/hpy/blob/master/proof-of-concept/pof.c
.. _`METH_FASTCALL`: https://www.python.org/dev/peps/pep-0580/


Sprint report and current status
---------------------------------

After this long preamble, here is a rough list of what we accomplished during
the week-long sprint and the days immediatly after.

On the HPy side, We kicked-off the code in the repo: at the moment of writing
the layout of the directories is a bit messy because we moved things around
several times, but identified several main sections:

  1. A specification of the API which serves both as documentation and as an
     input for parts of the projects which are automatically
     generated. Currently, this lives `public_api.h`_.

  2. A set of header files which can be used to compile extension modules:
     depending on whether the flag ``-DHPY_UNIVERSAL_ABI`` is passed to the
     compiler, the extension can target the `HPy/CPython ABI`_ or the `HPy
     Universal ABI`_

  3. A `CPython extension module`_ called ``hpy_universal`` which makes it
     possible to import universal modules on CPython

  4. A set of tests_ which are independent of the implementation and are meant
     to be an "executable specification" of the semantics.  Currently, these
     tests are run against three different implementations of the HPy API:

       - the headers which implements the "HPy/CPython ABI"

       - the ``hpy_universal`` module for CPython

       - the ``hpy_universal`` module for PyPy (these tests are run in the PyPy repo)

Moreover, we started a `PyPy branch`_ in which to implement the
``hpy_univeral`` module: at the moment of writing PyPy can pass all the HPy
tests apart the ones which allow conversion to and from ``PyObject *``.
Among the other things, this means that it is already possible to load the
very same binary module in both CPython and PyPy, which is impressive on its
own :).

Finally, we wanted a real-life use case to show how to port a module to HPy
and to do benchmarks.  After some searching, we choose ultrajson_, for the
following reasons:

  - it is a real-world extension module which was written with performance in
    mind

  - when parsing a JSON file it does a lot of calls to the Python API to
    construct the various parts of the result message

  - it uses only a small subset of the Python API

This repo contains the `HPy port of ultrajson`_. This commit_ shows an example
of what the porting looks like.

``ujson_hpy`` is also a very good example of incremental migration: so far
only ``ujson.loads`` is implemented using the HPy API, while ``ujson.dumps``
is still implemented using the old C-API, and both can coexist nicely in the
same compiled module.


.. _`public_api.h`: https://github.com/pyhandle/hpy/blob/9aa8a2738af3fd2eda69d4773b319d10a9a5373f/tools/public_api.h
.. _`CPython extension module`: https://github.com/pyhandle/hpy/tree/9aa8a2738af3fd2eda69d4773b319d10a9a5373f/cpython-universal/src
.. _`HPy/CPython ABI`: https://github.com/pyhandle/hpy/blob/9aa8a2738af3fd2eda69d4773b319d10a9a5373f/hpy-api/hpy_devel/include/cpython/hpy.h
.. _`HPy Universal ABI`: https://github.com/pyhandle/hpy/blob/9aa8a2738af3fd2eda69d4773b319d10a9a5373f/hpy-api/hpy_devel/include/universal/hpy.h
.. _tests: https://github.com/pyhandle/hpy/tree/9aa8a2738af3fd2eda69d4773b319d10a9a5373f/test

.. _`PyPy branch`: https://bitbucket.org/pypy/pypy/src/hpy/pypy/module/hpy_universal/

.. _ultrajson: https://github.com/esnme/ultrajson
.. _`HPy port of ultrajson`: https://github.com/pyhandle/ultrajson-hpy
.. _commit: https://github.com/pyhandle/ultrajson-hpy/commit/efb35807afa8cf57db5df6a3dfd4b64c289fe907


Benchmarks
-----------

Once we have a fully working ``ujson_hpy`` module, we can finally run
benchmarks!  We tested several different versions of the module:

  - ``ujson``: this is the vanilla implementation of ultrajson using the
    C-API. On PyPy this is executed by the infamous ``cpyext`` compatibility
    layer, so we expect it to be much slower than on CPython

  - ``ujson_hpy``: our HPy port compiled to target the HPy/CPython ABI. We
    expect it to be as fast as ``ujson``

  - ``ujson_hpy_universal``: same as above but compiled to target the
    Universal HPy ABI. We expect it to be slightly slower than ``ujson`` on
    CPython, and much faster on PyPy.

Finally, we also ran the benchmark using the builtin ``json`` module. This is
not really relevant to HPy, but it might still be an interesting as a
reference data point.

The benchmark_ is very simple and consists of parsing a `big JSON file`_ 100
times. Here is the average time per iteration (in milliseconds) using the
various versions of the module, CPython 3.7 and the latest version of the hpy
PyPy branch:

+---------------------+---------+--------+
|                     | CPython | PyPy   |
+---------------------+---------+--------+
| ujson               | 154.32  | 633.97 |
+---------------------+---------+--------+
| ujson_hpy           | 152.19  |        |
+---------------------+---------+--------+
| ujson_hpy_universal | 168.78  | 207.68 |
+---------------------+---------+--------+
| json                | 224.59  | 135.43 |
+---------------------+---------+--------+

As expected, the benchmark proves that when targeting the HPy/CPython ABI, HPy
doesn't impose any performance penalty on CPython. The universal version is
~10% slower on CPython, but gives an impressive 3x speedup on PyPy! It it
worth noting that the PyPy hpy module is not fully optimized yet, and we
expect to be able to reach the same performance as CPython for this particular
example (or even more, thanks to our better GC).

All in all, not a bad result for two weeks of intense hacking :)

It is also worth noting than PyPy's builtin ``json`` module does **really**
well in this benchmark, thanks to the recent optimizations that were described
in an `earlier blog post`_.


.. _benchmark: https://github.com/pyhandle/ultrajson-hpy/blob/hpy/benchmark/main.py
.. _`big JSON file`: https://github.com/pyhandle/ultrajson-hpy/blob/hpy/benchmark/download_data.sh
.. _`earlier blog post`: https://morepypy.blogspot.com/2019/10/pypys-new-json-parser.html


Conclusion and future directions
---------------------------------

We think we can be very satisfied about what we have got so far. The
development of HPy is quite new, but these early results seem to indicate that
we are on the right track to bring Python extensions into the future.

At the moment, we can anticipate some of the next steps in the development of
HPy:

  - Think about a proper API design: what we have done so far has
    been a "dumb" translation of the API we needed to run ``ujson``. However,
    one of the declared goal of HPy is to improve the design of the API. There
    will be a trade-off between the desire of having a clean, fresh new API
    and the need to be not too different than the old one, to make porting
    easier.  Finding the sweet spot will not be easy!

  - Implement the "debug" mode, which will help developers to find
    bugs such as leaking handles or using invalid handles.

  - Instruct Cython to emit HPy code on request.

  - Eventually, we will also want to try to port parts of ``numpy`` to HPy to
    finally solve the long-standing problem of sub-optimal ``numpy``
    performance in PyPy.

Stay tuned!
