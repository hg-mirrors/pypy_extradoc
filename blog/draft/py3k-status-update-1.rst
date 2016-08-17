Py3k status update
------------------

Thank to all the people who donated_ to the `py3k proposal`_, we managed to
collect enough money to start to work on the first step.  This is a quick
summary of what I did since I began working on this.

First of all, many thanks to Amaury Forgeot d'Arc, who started the `py3k
branch`_ months ago, and already implemented lots of features including
e.g. switching to "unicode everywhere" and the int/long unification, making my
job considerably easier :-)

I started to work on the branch at the last `Leysin sprint`_ together with
Romain Guillebert, where we worked on various syntactical changes such as
extended tuple unpacking and keyword-only arguments.  Working on such features
is a good way to learn about a lot of the layers which the PyPy Python
interpreter is composed of, because often you have to touch the tokenizer, the
parser, the ast builder, the compiler and finally the interpreter.

Then I worked on improving our test machinery in various way, e.g. by
optimizing the initialization phase of the object space created by tests,
which considerably speeds up small test runs, and adding the possibility to
automatically run our tests against CPython 3, to ensure that what we are not
trying to fix a test which is meant to fail :-). I also setup our buildbot to
run the `py3k tests nightly`_, so that we can have an up to date overview of
what is left to do.

Finally I started to look at all the tests in the interpreter/ directory,
trying to unmangle the mess of failing tests. Lots of tests were failing
because of simple syntax errors (e.g., by using the no longer valid ``except
Exception, e`` syntax or the old ``print`` statement), others for slightly
more complex reasons like ``unicode`` vs ``bytes`` or the now gone int/long
distinction.  Others were failing simply because they relied on new features,
such as the new `lexical exception handlers`_.

To give some numbers, at some point in january we had 1621 failing tests in
the branch, while today we are `under 1000`_ (to be exact: 999, and this is why
I've waited until today to post the status update :-)).

Before ending this blog post, I would like to thank once again all the people
who donated to PyPy, who let me to do this wonderful job.  That's all for now,
I'll post more updates soon.

cheers,
Antonio

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/src/py3k
.. _`Leysin sprint`: http://morepypy.blogspot.com/2011/12/leysin-winter-sprint.html
.. _`py3k tests nightly`: http://buildbot.pypy.org/summary?branch=py3k
.. _`lexical exception handlers`: http://bugs.python.org/issue3021
.. _`under 1000`: http://buildbot.pypy.org/summary?category=linux32&branch=py3k&recentrev=52508:c1756f5aa63e


