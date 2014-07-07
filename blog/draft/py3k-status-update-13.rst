Py3k status update #13
----------------------

This is the 13th status update about our work on the `py3k branch`_, which we
can work on thanks to all of the people who donated_ to the `py3k proposal`_.

We're just finishing up a cleanup of int/long types. This work helps the py3k
branch unify these types into the Python 3 int and restore `JIT compilation of
machine sized integers`_.

This cleanup also removes `multimethods`_ from these types. PyPy has
historically used a clever implementation of multimethod dispatch for declaring
methods of the __builtin__ types in RPython.

This multimethod scheme provides some convenient features for doing this,
however we've come to the conclusion that it may be more trouble than it's
worth. A major problem of multimethods is that they generate a large amount of
stub methods which burden the already lengthy and memory hungry RPython
translation process. Also, their implementation and behavior can be somewhat
complicated/obscure.

The alternative to multimethods involves doing the work of the type checking
and dispatching rules in a more verbose, manual way. It's a little more work in
the end but less magical.

Recently, Manuel Jacob finished a large cleanup effort of the
unicode/string/bytearray types that also removed their multimethods. This work
also benefits the py3k branch: it'll help with future `PEP 393`_ (or `PEP 393
alternative`_) work. This effort was partly sponsored by Google's Summer of
Code: thanks Manuel and Google!

Now there's only a couple major pieces left in the multimethod removal (the
float/complex types and special marshaling code) and a few minor pieces that
should be relatively easy.

In conclusion, there's been some good progress made on py3k and multimethod
removal this winter, albeit a bit slower than we would have liked.

cheers,
Phil

.. _donated: http://morepypy.blogspot.com/2012/01/py3k-and-numpy-first-stage-thanks-to.html
.. _`py3k proposal`: http://pypy.org/py3donate.html
.. _`py3k branch`: https://bitbucket.org/pypy/pypy/commits/all/tip/branch%28%22py3k%22%29

.. _`JIT compilation of machine sized integers`:
    http://morepypy.blogspot.com/2013/11/py3k-status-update-12.html
.. _`multimethods`: http://doc.pypy.org/en/latest/objspace.html#multimethods

.. _`PEP 393`: http://www.python.org/dev/peps/pep-0393/
.. _`PEP 393 alternative`: http://lucumr.pocoo.org/2014/1/9/ucs-vs-utf8/
