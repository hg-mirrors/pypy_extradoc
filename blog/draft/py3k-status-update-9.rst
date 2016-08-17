Py3k status update #9
---------------------

This is the ninth status update about our work on the `py3k branch`_, which
we can work on thanks to all of the people who donated_ to the `py3k
proposal`_.

Just a very short update on December's work: we're now passing about 223 of
approximately 355 modules of CPython's regression test suite, up from passing
194 last month.

Some brief highlights:

* More encoding related issues were addressed. e.g. now most if not all the
  multibytecodec test modules pass.

* Fixed some path handling issues (``test_os``, ``test_ntpath`` and
  ``test_posixpath`` now pass)

* We now pass ``test_class``, ``test_descr`` and almost ``test_builtin`` (among
  other things): these are notable as they are fairly extensive test suites of
  core aspects of the langauge.

* Amaury Forgeot d'Arc continued making progress on `CPyExt`_ (thanks again!)

cheers,
Phil

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/commits/all/tip/branch%28%22py3k%22%29
.. _`CPyExt`: http://morepypy.blogspot.com/2010/04/using-cpython-extension-modules-with.html
