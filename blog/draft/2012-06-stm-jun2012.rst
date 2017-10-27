STM with threads
================

Hi all,

A quick update.  The first version of pypy-stm `based on regular
threads`_ is ready.  Still having no JIT and a 4-or-5-times performance
hit, it is not particularly fast, but I am happy that it turns out not
to be much slower than the previous thread-less attempts.  It is at
least fast enough to run faster (in real time) than an equivalent no-STM
PyPy, if fed with an eight-threaded program on an eight-core machine
(provided, of course, you don't mind it eating all 8 cores' CPU power
instead of just one :-).

You can download and play around with `this binary`_ for Linux 64.  It
was made from the `stm-thread`_ branch of the PyPy repository.  (Be sure
to put it where it can find its stdlib, e.g. by putting it inside the
directory from the official `1.9 release`_.)  

This binary supports the ``thread`` module and runs without the GIL.
So, despite the factor-of-4 slow-down issue, it should be the *fourth*
complete Python interpreter in which we can reasonably claim to have
resolved the problem of the GIL.  (The first one was Greg Stein's Python
1.4, re-explored here_; the second one is Jython_; the third one is
IronPython_.)  Unlike the previous three, it is also the first one to
offer full GIL semantics to the programmer, and additionally
``thread.atomic`` (see below).  I should also add that we're likely to
see in the next year a 5th such interpreter, too, based on Hardware
Transactional Memory (same approach as with STM, but using e.g.
`Intel's HTM`_).

The binary I linked to above supports all built-in modules from PyPy,
apart from ``signal``, still being worked on (which can be a bit
annoying because standard library modules like ``subprocess`` depend on
it).  The ``sys.get/setcheckinterval()`` functions can be used to tweak
the frequency of the automatic commits.  Additionally, it offers
``thread.atomic``, described in the `previous blog post`_ as a way to
create longer atomic sections (with the observable effect of preventing
the "GIL" to be released during that time).  A complete
``transaction.py`` module based on it is available `from the sources`_.

The main missing features are:
  
- the ``signal`` module;

- the Garbage Collector, which does not do major collections so far, only
  minor ones;

- and finally, the JIT, which needs some amount of integration to generate
  the correctly-tweaked assembler.

Have fun!


Armin.


.. _`based on regular threads`: http://morepypy.blogspot.ch/2012/05/stm-update-back-to-threads.html
.. _`previous blog post`: http://morepypy.blogspot.ch/2012/05/stm-update-back-to-threads.html
.. _`this binary`: http://cobra.cs.uni-duesseldorf.de/~buildmaster/misc/pypy-stm-38eb1fbc3c8d.bz2
.. _`1.9 release`: https://bitbucket.org/pypy/pypy/downloads/pypy-1.9-linux64.tar.bz2
.. _`stm-thread`: https://bitbucket.org/pypy/pypy/src/stm-thread
.. _`from the sources`: https://bitbucket.org/pypy/pypy/src/stm-thread/lib_pypy/transaction.py
.. _`since long ago`: http://dabeaz.blogspot.ch/2011/08/inside-look-at-gil-removal-patch-of.html
.. _here: http://dabeaz.blogspot.ch/2011/08/inside-look-at-gil-removal-patch-of.html
.. _Jython: http://jython.org/
.. _IronPython: http://ironpython.net/
.. _`Intel's HTM`: http://software.intel.com/en-us/blogs/2012/02/07/transactional-synchronization-in-haswell/
