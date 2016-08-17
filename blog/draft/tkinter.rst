Using Tkinter and IDLE with PyPy
=================================

We are pleased to announce that Tkinter, the GUI library based on TCL/TK, now
works with PyPy.

Tkinter is composed of two parts:

  - ``_tkinter``, a module written in C which interfaces with the TCL world

  - ``Tkinter``, a pure Python package which wraps ``_tkinter`` to expose the
    pythonic API we are used to

The `PyPy version of _tkinter`_ reuses the C code of as found in CPython and
compile it through the PyPy C-API compatibility layer, ``cpyext``.  To make it
work with PyPy, we had to modify it slightly, in order to remove the
dependency on some API functions which are not supported by PyPy.  In particular, we
removed the dependency on the ``PyOS_InputHook`` variable, which allows a nice
integration of Tkinter and the Python interactive prompt: the result is that,
unlike CPython, in PyPy Tk windows created at the interactive prompt are not
shown until we manually call the ``mainloop`` method.  Apart from this
inconvenience, all the rest works fine.

At the moment, ``_tkinter`` is not distributed with PyPy because our build
system does not support automatic compilation of C extension.  Instead, it is
necessary to install it manually, either directly from source_ or by
easy_installing/pip installing `tkinter-pypy`_ from PyPI.

For everything to work correctly, you need a recent build of PyPy: the
following is a step-by-step guide to install ``_tkinter`` in a PyPy nightly
build for Linux 64 bit; for other architectures, look at the `nightly build
page`_::

  $ wget http://buildbot.pypy.org/nightly/trunk/pypy-c-jit-43485-1615dfd7d8f1-linux64.tar.bz2

  $ tar xfv pypy-c-jit-43485-1615dfd7d8f1-linux64.tar.bz2

  $ cd pypy-c-jit-43485-1615dfd7d8f1-linux64/

  $ wget http://peak.telecommunity.com/dist/ez_setup.py

  $ ./bin/pypy ez_setup.py    # install setuptools

  $ ./bin/easy_install tkinter-pypy

Once you complete the steps above, you can start using ``Tkinter`` from your
python programs.  In particular, you can use IDLE, the IDE which is part of
the Python standard library.  To start IDLE, type::

  $ ./bin/pypy -m idlelib.idle

Have fun :-)

.. _`PyPy version of _tkinter`: http://bitbucket.org/pypy/tkinter
.. _source: http://bitbucket.org/pypy/tkinter
.. _`tkinter-pypy`: http://pypi.python.org/pypi/tkinter-pypy/

http://buildbot.pypy.org/nightly/trunk/pypy-c-jit-43478-f8c673fee06d-linux.tar.bz2
