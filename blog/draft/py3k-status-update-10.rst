Py3k status update #10
----------------------

This is the tenth status update about our work on the `py3k branch`_, which we
can work on thanks to all of the people who donated_ to the `py3k proposal`_.

There's been significant progress since the last update: the `linux x86-32
buildbot`_ now passes 289 out of approximately 354 modules (with 39 skips) of
CPython's regression test suite.

That means there's only 26 test module failures left! The list of major items
remaining for 3.2 compatibility are now short enough to list here, with their
related tests:

* Tokenizer support for non-ascii identifiers

 - test_importlib
 - test_pep263

* memoryview (Manuel Jacob's tackling this on the `py3k-memoryview branch`_)

 - test_memoryview

* multiprocessing module currently deadlocks

 - test_multiprocessing

* Buggy handling of the new extended unpacking syntax by the compiler:

 - test_unpack_ex

* The new Global Interpreter Lock and new thread signal handling

 - test_threading
 - test_threadsignals
 - test_sys

* Upgrade unicodedata to 6.0.0 (requires updates to the actual unicodedata
  generation script)

 - test_ucn
 - test_unicode
 - test_unicodedata

* `CPyExt`_

 - test_capi (currently crashes)

* Update int's hash code to match to CPython (float's is already updated on the
  `py3k-newhash branch`_. note that PyPy 2.x doesn't even totally match
  CPython's hashing)

 - test_decimal
 - test_fractions
 - test_numeric_tower

* Miscellaneous:

 - test_complex
 - test_float
 - test_peepholer
 - test_range
 - test_sqlite (a new cffi based version seems to be coming)
 - test_ssl
 - test_struct
 - test_subprocess
 - test_sys_settrace
 - test_time

Additionally there are still a number of failures in PyPy's internal test
suite. These tests are usually ran against untranslated versions of PyPy during
development. However we've now began running them against a fully translated
version of PyPy on the buildbot too (thanks to Amaury for setting this
up). This further ensures that our tests and implementation are sane.

We're getting closer to producing an initial alpha release. Before that happens
we'd like to see:

* further test fixes
* the results of test runs on other major platforms (e.g. linux x86-64 and osx
  seem to have some additional failures as of now)
* some basic real world testing

Finally I'd like to thank Manuel Jacob for his various contributions over the
past month, including fixing the array and ctypes modules among other things,
and also Amaury Forgeot d'Arc for his ongoing excellent contributions.

cheers,
Phil

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/commits/all/tip/branch%28%22py3k%22%29
.. _`CPyExt`: http://morepypy.blogspot.com/2010/04/using-cpython-extension-modules-with.html
.. _`linux x86-32 buildbot`: http://buildbot.pypy.org/summary?branch=py3k
.. _`py3k-memoryview branch`: https://bitbucket.org/pypy/pypy/compare/py3k-memoryview..py3k
.. _`py3k-newhash branch`: https://bitbucket.org/pypy/pypy/compare/py3k-newhash..py3k
