Visualization of JITted code
============================

Hello.

We're proud to announce the first public release of the jitviewer. As of now,
jitviewer is a slightly internal tool that helps understanding how your Python 
source code is compiled by the PyPy's JIT all the way down to machine code.

To install it, you need a very recent version of PyPy
(newer than 9th of August), for example one of the `nightly builds`_: 

  - install ``pip`` and ``distribute`` either by creating a PyPy virtualenv_
    or by following the `installation instructions`_.

  - make sure to have a `source code checkout`_ of PyPy and put it in your
    PYTHONPATH.

  - ``pip install jitviewer``.  Note that you need to run the ``pip``
    executable which belongs to PyPy, not the globally installed one.

Have a look at the README_ for how to start it, or try the `online demo`_ if
you just want to play with it.

The jitviewer is a web application written with ``flask`` and ``jinja2``.  If
you have experience with web development and you want to help PyPy, don't
hesitate to contact us, there are plenty of things to improve in it :-).

.. _`source code checkout`: http://bitbucket.org/pypy/pypy
.. _`nightly builds`: http://buildbot.pypy.org/nightly/trunk/
.. _`online demo`: http://wyvern.cs.uni-duesseldorf.de:5000/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _`installation instructions`: http://doc.pypy.org/en/latest/getting-started.html#installing-pypy
.. _README: http://bitbucket.org/pypy/jitviewer/src/24adc3403cd8/README


What does the jitviewer really do?
----------------------------------

At the top of the page, you will see the list of pieces of code which has been
compiled by the JIT.  You will see entries for both normal loops and for
"entry bridges".  This is not the right place to discuss the difference
between those, but you most probably want to look at loops, because usually
it's where most of the time is spent.

Note that for each loop, you will see the name of the function which contains
the **first** instruction of the loop.  However, thanks to the inlining done
by the JIT, it will contain also the code for other functions.

Once you select a loop, the jitviewer shows how the JIT has compiled the
Python source code into assembler in a hierarchical way. It displays four
levels:

* Python source code: only the lines shown in azure have been compiled for
  this particular loop, the ones in gray have not.

* Python bytecode, the one you would get by doing::

   def f(a, b):
      return a + b

   import dis
   dis.dis(f)

  The opcodes are e.g. ``LOAD\_FAST``, ``LOAD\_GLOBAL`` etc.  The opcodes
  which are not in bold have been completely optimized aways by the JIT.

* Intermediate representation of jit code (IR). This is a combination of
  operations (like integer addition, reading fields out of structures) and
  guards (which check that the assumptions we made are actually true). Guards
  are in red.  These operations are "at the same level as C": so, for example,
  ``+`` takes two unboxed integers which can be stored into the register
  of the CPU.

* Assembler: you can see it by clicking on "Show assembler" in the menu on the
  right.

Sometimes you'll find that a guard fails often enough that a new piece of
assembler is required to be compiled. This is an alternative path through the
code and it's called a bridge. You can see bridges in the jitviewer when
there is a link next to a guard. For more information about purpose look up
the `jit documentation`_.

.. _`jit documentation`: http://doc.pypy.org/en/latest/jit/index.html


I'm still confused
------------------

Jitviewer is not perfect when it comes to explaining what's going on. Feel free
to pop up on IRC or send us a mail to the mailing list, we'll try to explain
and/or improve the situation. Consult the `contact`_ page for details.

.. _`contact`: http://pypy.org/contact.html

Cheers,
fijal & antocuni
