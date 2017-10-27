Py3k status update #4
---------------------

This is the fourth status update about our work on the `py3k branch`_, which we
can work on thanks to all of the people who donated_ to the `py3k proposal`_.

For various reasons, less work than usual has been done since the last status
update. However, some interesting things happened anyway.

As readers know, so far we spent most of the effort in fixing all PyPy's own
tests which started to fail for various py2/py3 differences.  Most of them
failed for shallow reasons, e.g. syntactic changes or the int/long
unifications. Others failed for subtle differences and needed a bit more care,
for example the fact that unbound methods are gone in Py3k.

The good news is that finally we are seeing the light at the end of the
tunnel. Most of them have been fixed. For sine other tests, we introduced the
concept of "py3k-skipping": some optimizations and modules are indeed failing,
but right now we are concentrating on completing the core language and so we
are not interested in those.  When the core language will be done, we will be
able to easily find and work on the py3k-skipped tests.  In particular, for
now we disabled the ``Int`` and ``String`` dict strategies, which are broken
because of the usual int/long unification and str vs bytes.  As for modules,
for now ``_continuation`` (needed for stackless) and ``_multiprocessing`` do
not work yet.

Another non-trivial feature we implemented is the proper cleaning of exception
variables when we exit ``except`` blocks.  This is a feature which touches
lots of levels of PyPy, starting from ``astcompiler``, down to the bytecode
interpreter. It tooks two days of headache, but at the end we made it :-).

Additionally, Amaury did a lot of improvements to ``cpyext``, which had been
broken since forever on this branch.

As for the next plans, now that things are starting to work and PyPy's own
tests mostly pass, we can finally start to run the compiled PyPy against
CPython's test suite.  It is very likely that we will have tons of failures at
the beginning, but once we start to fix them one by one, a Py3k-compatible
PyPy will be closer and closer.

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/src/py3k
