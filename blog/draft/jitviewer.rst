Visualization of JITted code
============================

Hello.

We're proud to announce the first public release of the jitviewer. As of now,
jitviewer is a slightly internal tool that helps understanding how PyPy's JIT
compiles Python down all the way to assembler. If you want to give it a go,
clone the `repository`_ and look up the README. You also need both the PyPy
`source code checkout`_ and a fairly recent compiled PyPy executable, like
`a nightly`_ one. If you want to look first what does it do, check out
`the online demo`_.

.. _`repository`: http://bitbucket.org/pypy/jitviewer
.. _`source code checkout`: http://bitbucket.org/pypy/pypy
.. _`a nightly`: http://buildbot.pypy.org/nightly/trunk/
.. _`the online demo`: http://wyvern.cs.uni-duesseldorf.de:5000/

What does the jitviewer really do?
----------------------------------

In short - it displays how exactly the JIT has compiled python source code
into assembler in a hierarchical way. It displays four levels:

* Python source code

* Python bytecode, the one you would get by doing::

   def f(a, b):
      return a + b

   import dis
   dis.dis(f)

  This looks like LOAD\_FAST, LOAD\_GLOBAL etc.

* Intermediate representation of jit code (IR). This is a combination of
  operations (like integer addition, reading fields out of structures) and
  guards (aborting assembler if invariants are invalidated). Guards are in red.
  Those operations operate on machine-level objects, like integers and memory
  locations.

* Assembler

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
fijal
