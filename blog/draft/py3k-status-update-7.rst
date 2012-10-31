Py3k status update #7
---------------------

This is the seventh status update about our work on the `py3k branch`_, which
we can work on thanks to all of the people who donated_ to the `py3k
proposal`_.

The biggest news is that this month Philip started to work on py3k in parallel
to Antonio. As such, there was an increased amount of activity.

The `py3k buildbots`_ now fully translate the branch every night and run the
Python standard library tests.

We currently pass 160 out of approximately 355 modules of CPython's standard
test suite, fail 144 and skip apprixmately 51.

Some highlights:

o dictviews (the objects returned by dict.keys/values/items) has been greatly
  improved, and now they full support set operators

o a lot of tests has been fixed wrt complex numbers (and in particular the
``__complex__`` method)

o _csv has been fixed and now it correctly handles unicode instead of bytes

o more parser fixes, py3k list comprehension semantics; now you can no longer
  access the list comprehension variable after it finishes

o 2to3'd most of our custom lib_pypy

o py3-enabled pyrepl: this means that finally readline works at the command
  prompt, as well as builtins.input(). ``pdb`` seems to work, as well as
  fancycompleter_ to get colorful TAB completions :-)

o py3 round

o further tightening/cleanup of the unicode handling (more usage of
surrogateescape, surrogatepass among other things)

o as well as keeping up with some big changes happening on the default branch

Finally, I would like to thank Amaury Forgeot d'Arc for his significant
contributions; among other things, Amaury recently worked on <all kinds of
stuff listed above>


cheers,
Philip&Antonio

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/src/py3k
.. _`py3k buildbots`: http://buildbot.pypy.org/summary?branch=py3k
