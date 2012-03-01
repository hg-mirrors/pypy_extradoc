Py3k status update #2
---------------------

This is the second status update about my work on the `py3k branch`_, which I
can work on thanks to all of the people who donated_ to the `py3k proposal`_.

Since my previous `status update`_, things have improved a lot: first of all, I
fixed the syntax of many more tests, which were failing on the branch because
they used constructs which are no longer valid in Python 3, such as ``u''``
strings, the ``print`` statement or the old ``except Exception, e`` syntax.  I
have to say that this work is tedious and not very rewarding, but it has to be
done anyway, so that the real failures can stand up.

Then, I spent most of the rest of the time by killing features which are
present in Python 2 and are gone in Python 3.

Some of them were easy and mechnical: for example, I removed all the function
attributes such as ``func_code`` and ``func_closure``, which has been renamed
to ``__code__`` and ``__closure__``, and then I had to find and fix all the
places which still expected the old ones.

Some were trickier: I removed support for the ``cmp`` function and the
``__cmp__`` special method, but this also meant that I had to fix a few types
which relied on it to be comparable (for example, did you know that the cells
contained in ``__closure__`` are comparable?). At the same time, I also
removed the old behavior which in Python 2 allows us to compare arbitrary
objects with ``<``, ``>`` & co.: in Python 3 the only comparisons allowed
between incompatible types are ``==`` and ``!=``.

Speaking of old special methods, ``__hex__`` and ``__oct__`` are gone as well
(and I didn't even know about their existence before removing them :-))

But the most important breakthrough was the removal of the ``_file`` module,
containing the implementation of the ``file`` type in Python 2, which is now
gone since in Python 3 files are handled by the ``_io`` module.  Killing the
module was not straightforward, because some of the importing logic was tightly
tied to the internal implementation of files, so it needed some refactoring.
Finally, I had to fix the ``marshal`` module to correctly detect text files
vs. byte files.

Among these things, I fixed tons of smaller issues here and there. As a
result, there are many fewer failing tests than a few weeks ago.  Obviously the
number itself does not mean much, because sometimes fixing a single test takes
hours, and some other times by changing one line one fixes tens of tests. But at
the end, seeing it dropping from 999 to 650_ always is nice and rewarding :-).

The road for having a pypy3k is still long, but everything is going fine so
far. Stay tuned for more updates!

cheers,
Antonio

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/src/py3k
.. _`status update`: http://morepypy.blogspot.com/2012/02/py3k-status-update.html
.. _650: http://buildbot.pypy.org/summary?category=linux32&branch=py3k&recentrev=53071:411bb6d819b1
