Py3k status update #7
---------------------

This is the seventh status update about our work on the `py3k branch`_, which
we can work on thanks to all of the people who donated_ to the `py3k
proposal`_.

There was an increased amount of activity this month.

The `py3k buildbots`_ now fully translate the branch every night and run the
Python standard library tests.

We currently pass 160 out of approximately 355 test modules, fail 144 and skip
apprixmately 51.

o work on dictviews (keys/values/items)

o _csv

o more parser fixes, py3 list comprehension semantics

o 2to3'd most of our custom lib_pypy

o py3-enabled pyrepl (readline works in the repl!), builtins.input() (pdb seems to work!)

o py3 round

o further tightening/cleanup of the unicode handling (more usage of
surrogateescape, surrogatepass among other things)

o as well as keeping up with some big changes happening on the default branch

Finally, I would like to thank Amaury Forgeot d'Arc for his significant
contributions; among other things, Amaury recently worked on <all kinds of
stuff listed above>

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/src/py3k
.. _`py3k buildbots`: http://buildbot.pypy.org/summary?branch=py3k
