Py3k status update #6
---------------------

This is the sixth status update about our work on the `py3k branch`_, which we
can work on thanks to all of the people who donated_ to the `py3k proposal`_.

The coolest news is not about what we did in the past weeks, but what we will
do in the next: I am pleased to announce that `Philip Jenvey`_ has been
selected by the PyPy communitiy to be funded for his upcoming work on py3k,
thanks to your generous donations. He will start to work on it shortly, and he
will surely help the branch to make faster progress.  I am also particularly
happy of this because Philip is the first non-core developer who is getting
paid with donations: he demonstrated over the past months to be able to work
effectively on PyPy, and so we were happy to approve his application for the
job.  This means that anyone can potentially be selected in the future, the
only strict requirement is to have a deep interest in working on PyPy and to
prove to be able to do so by contributing to the project.

Back to the status of the branch. Most of the work since the last status
update has been done in the area of, guess what? Unicode strings. As usual,
this is one of the most important changes between Python 2 and Python 3, so
it's not surprising.  The biggest news is that now PyPy internally supports
unicode identifiers (such as names of variables, functions, attributes, etc.),
whereas earlier it supported only ASCII bytes strings.  The changes is still
barely visible from the outside, because the parser still rejects non-ASCII
identifiers, however you can see it with a bit of creativity::

    >>>> def foo(x): pass
    >>>> foo(**{'àèìòù': 42})      
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
    TypeError: foo() got an unexpected keyword argument 'àèìòù'

Before the latest changes, you used to get question marks instead of the
proper name for the keyword argument.  Although this might seem like a small
detail, it is a big step towards a proper working Python 3 interpreter and it
required a couple of days of headaches.  A spin-off of this work is that now
RPython has better built-in support for unicode (also in the default branch):
for example, it now supports unicode string formatting (using the percent
operator) and the methods ``.encode/.decode('utf-8')``.

Other than that there is the usual list of smaller issues and bugs that got
fixed, including (but not limited to):

  - teach the compiler when to emit the new opcode ``DELETE_DEREF`` (and
    implement it!)

  - detect when we use spaces and TABs inconsistently in the source code, as
    CPython does

  - fix yet another bug related to the new lexically scoped exceptions (this
    is the last one, hopefully)

  - port some of the changes that we did to the standard CPython 2.7 tests to
    3.2, to mark those which are implementation details and should not be run on
    PyPy

Finally, I would like to thank Amaury Forgeot d'Arc and Ariel Ben-Yehuda for
their work on the branch; among other things, Amaury recently worked on
``cpyext`` and on the PyPy ``_cffi_backend``, while Ariel submitted a patch to
implement `PEP 3138`.

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/src/py3k
.. _`PEP 3138`: http://www.python.org/dev/peps/pep-3138/
.. _`Philip Jenvey`: https://twitter.com/pjenvey
