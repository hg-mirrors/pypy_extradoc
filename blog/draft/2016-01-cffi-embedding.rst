========================
Using CFFI for embedding
========================

CFFI_ has been a great success so far to call C libraries in your
Python programs, in a way that is both simple and that works across
CPython 2.x and 3.x and PyPy.

This post assumes that you know what CFFI is and how to use it in
API mode (``ffi.cdef()``, ``ffi.set_source()``, ``ffi.compile()``).
A quick overview can be found here__.

The major news of CFFI 1.4, released last december, was that you can
now declare C functions with ``extern "Python"``, in the ``cdef()``.
These magic keywords make the function callable from C (where it is
defined automatically), but calling it will call some Python code
(which you attach with the ``@ffi.def_extern()`` decorator).  This is
useful because it gives a more straightforward, faster and
libffi-independent way to write callbacks.  For more details, see `the
documentation`_.

You are, in effect, declaring a static family of C functions which
call Python code.  The idea is to take pointers to them, and pass them
around to other C functions, as callbacks.  However, the idea of a set
of C functions which call Python code opens another path: *embedding*
Python code inside non-Python programs.

Embedding is traditionally done using the CPython C API: from C code,
you call ``Py_Initialize()`` and then some other functions like
``PyRun_SimpleString()``.  In the simple cases it is, indeed, simple
enough; but it can become a complicated story if you throw in
supporting application-dependent object types; and a messy story if
you add correctly running on multiple threads, for example.

Moreover, this approach is specific to CPython (2.x or 3.x).  It does
not work at all on PyPy, which has its own very different, minimal
`embedding API`_.

The new-and-coming thing about CFFI 1.5, meant as replacement of the
above solutions, is direct embedding support---with no fixed API at
all.  The idea is to write some Python script with a ``cdef()`` which
declares a number of ``extern "Python"`` functions.  When running the
script, it creates the C source code and compiles it to a
dynamically-linked library (``.so`` on Linux).  This is the same as in
the regular API-mode usage.  What is new is that these ``extern
"Python"`` can now also be *exported* from the ``.so``, in the C
sense.  You also give a bit of initialization-time Python code
directly in the script, which will be compiled into the ``.so`` too.

This library can now be used directly from any C program (and it is
still importable in Python).  It exposes the C API of your choice,
which you specified with the ``extern "Python"`` declarations.  You
can use it to make whatever custom API makes sense in your particular
case.  You can even directly make a "plug-in" for any program that
supports them, just by exporting the API expected for such plugins.

This is still being finalized, but please try it out.  (You can also
see `embedding.py`_ directly online for a quick glance.)  See
below the instructions on Linux with CPython 2.7 (CPython 3.x and
non-Linux platforms are still a work in progress right now, but this
should be quickly fixed):

* get the branch ``static-callback-embedding`` of CFFI::

      hg clone https://bitbucket.org/cffi/cffi
      hg up static-callback-embedding

* make the ``_cffi_backend.so``::

      python setup_base.py build_ext -f -i

* run ``embedding.py`` in the ``demo`` directory::

      cd demo
      PYTHONPATH=.. python embedding.py

* this produces ``_embedding_cffi.c``; run ``gcc`` to build it---on Linux::

      gcc -shared -fPIC _embedding_cffi.c -o _embedding_cffi.so -lpython2.7 -I/usr/include/python2.7

* try out the demo C program in ``embedding_test.c``::

      gcc embedding_test.c _embedding_cffi.so
      PYTHONPATH=.. LD_LIBRARY_PATH=. a.out

Note that if you get ``ImportError: cffi extension module
'_embedding_cffi' has unknown version 0x2701``, it means that the
``_cffi_backend`` module loaded is a pre-installed one instead of the
more recent one in ``..``.  Be sure to use ``PYTHONPATH=..`` for now.

Very similar steps can be followed on PyPy, but it requires the
``cffi-static-callback-embedding`` branch of PyPy, which you must
first translate from sources.  The difference is then that you need to
adapt the first ``gcc`` command line: replace ``-lpython2.7`` with
``-lpypy-c`` and to fix the ``-I`` path (and possibly add a ``-L``
path).

Note that CPython/PyPy is automatically initialized (using locks in case
of multi-threading) the first time any of the ``extern "Python"``
functions is called from the C program.  (This should work even if two
different threads call the first time a function from two *different*
embedded CFFI extensions; in other words, explicit initialization is
never needed).  The custom initialization-time Python code you put in
``ffi.embedding_init_code()`` is executed at that time.  If this code
starts to be big, you can move it to independent modules or packages.
Then the initialization-time Python code only needs to import them.  In
that case, you have to carefully set up ``sys.path`` if the modules are
not installed in the usual Python way.

If the Python code is big and full of dependencies, a better alternative
would be to use virtualenv.  How to do that is not fully fleshed out so
far.  You can certainly run the whole program with the environment
variables set up by the virtualenv's ``activate`` script first.  There
are probably other solutions that involve using gcc's
``-Wl,-rpath=\$ORIGIN/`` or ``-Wl,-rpath=/fixed/path/`` options to load
a specific libpython or libypypy-c library.  If you try it out and it
doesn't work the way you would like, please complain ``:-)``

Another point: right now this does not support CPython's notion of
multiple subinterpreters.  The logic creates a single global Python
interpreter, and runs everything in that context.  Maybe a future
version would have an explicit API to do that---or maybe it should be
the job of a 3rd-party extension module to provide a Python interface
over the notion of subinterpreters...

More generally, any feedback is appreciated.


Have fun,

Armin
