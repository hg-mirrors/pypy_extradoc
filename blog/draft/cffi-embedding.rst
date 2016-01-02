========================
Using CFFI for embedding
========================

CFFI_ has been a great success so far to call C libraries in your
Python programs, in a way that is both simple and that works across
CPython 2.x and 3.x and PyPy.

We are now adding support for *embedding* Python inside non-Python
programs.  This is traditionally done using the CPython C API: from C
code, you call ``Py_Initialize()`` and then some other functions like
``PyRun_SimpleString()``.  In the simple cases it is, indeed, simple
enough; but it can become a more complicated story if you throw in
supporting application-dependent object types, and correctly running
on multiple threads, and so on.

Moreover, this approach is specific to CPython (2.x or 3.x, which you
can do in a similar way).  It does not work on PyPy, which has its own
smaller `embedding API`_.

The new-and-coming thing about CFFI, meant as replacement of the above
solutions, is direct embedding support---and it does that with no
fixed API at all.  The idea is to write some Python script with a
``cdef()`` which declares a number of ``extern "Python"`` functions.
When running the script, it creates the C source code and compiles it
to a dynamically-linked library (``.so`` on Linux).  This is the same
as in the regular API-mode usage, and ``extern "Python"`` was
`introduced in CFFI 1.4`_.  What is new is that these ``extern
"Python"`` can now also be *exported* from the ``.so``, in the C
sense.  You also give a bit of initialization-time Python code
directly in the script, which will be compiled into the ``.so``
too.

In other words, this library can now be used directly from any C
program (and it is still importable in Python).  It exposes the C API
of your choice, which you specified with the ``extern "Python"``
declarations.  You can use it to make whatever custom API makes sense
in your particular case.  You can even directly make a "plug-in" for
any program that supports them, just by exporting the API expected for
such plugins.

This is still being finalized, but please try it out.  (You can also
see `embedding.py`_ directly online for a quick glance.)  These are
the instructions on Linux with CPython 2.7::

* get the branch ``static-callback-embedding`` of CFFI::

      hg clone https://bitbucket.org/cffi/cffi
      hg up static-callback-embedding

* make the ``_cffi_backend.so``::

      python setup_base.py build_ext -f -i

* run ``embedding.py`` in the ``demo`` directory::

      cd demo
      PYTHONPATH=.. python embedding.py

* run ``gcc`` to build the C sources---on Linux::

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
first translate from sources.

CPython 3.x and non-Linux platforms are still a work in progress right
now, but this should be quickly fixed.

Note that CPython/PyPy is automatically initialized (using locks in
case of multi-threading) the first time any of the ``extern "Python"``
functions is called from the C program.  At that time, the custom
initialization-time Python code you put in
``ffi.embedding_init_code()`` is executed.  If this code starts to be
big, you may consider moving it to independent modules or packages;
then the initialization-time Python code only needs to import them
(possibly after hacking around with ``sys.path``).

Another point: right now this does not support CPython's notion of
multiple subinterpreters.  The logic creates a single global Python
interpreter, and runs everything in that context.  Idea about how to
support that cleanly would be welcome ``:-)`` More generally, any
feedback is appreciated.


Have fun,

Armin
