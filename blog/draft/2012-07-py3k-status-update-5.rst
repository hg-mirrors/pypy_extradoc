Py3k status update #5
---------------------

This is the fifth status update about our work on the `py3k branch`_, which we
can work on thanks to all of the people who donated_ to the `py3k proposal`_.

Apart from the usual "fix shallow py3k-related bugs" part, most of my work in
this iteration has been to fix the bootstrap logic of the interpreter, in
particular to setup the initial ``sys.path``.

Until few weeks ago, the logic to determine ``sys.path`` was written entirely
at app-level in ``pypy/translator/goal/app_main.py``, which is automatically
included inside the executable during translation.  The algorithm is more or
less like this:

  1. find the absolute path of the executable by looking at ``sys.argv[0]``
     and cycling through all the directories in ``PATH``

  2. starting from there, go up in the directory hierarchy until we find a
     directory which contains ``lib-python`` and ``lib_pypy``

This works fine for Python 2 where the paths and filenames are represented as
8-bit strings, but it is a problem for Python 3 where we want to use unicode
instead.  In particular, whenever we try to encode a 8-bit string into an
unicode, PyPy asks the ``_codecs`` built-in module to find the suitable
codec. Then, ``_codecs`` tries to import the ``encodings`` package, to list
all the available encodings. ``encodings`` is a package of the standard
library written in pure Python, so it is located inside
``lib-python/3.2``. But at this point in time we yet have to add
``lib-python/3.2`` to ``sys.path``, so the import fails.  Bootstrap problem!

The hard part was to find the problem: since it is an error which happens so
early, the interpreter is not even able to display a traceback, because it
cannot yet import ``traceback.py``. The only way to debug it was through some
carefully placed ``print`` statement and the help of ``gdb``. Once found the
problem, the solution was as easy as moving part of the logic to RPython,
where we don't have bootstrap problems.

Once the problem was fixed, I was able to finally run all the CPython test
against the compiled PyPy.  As expected there are lots of failures, and fixing
them will be the topic of my next months.


.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/src/py3k
