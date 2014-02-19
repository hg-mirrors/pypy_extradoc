How to install NumPy on PyPy
============================

* Debian, Ubuntu and maybe others: make sure to run
  ``apt-get install pypy-dev``.  The Debian package is, as usual, split
  into more pieces than we'd like.  You get it all in one go if you
  installed PyPy any other way.

* Windows: you may or may not need to edit the file ``include/Python.h``
  from your PyPy installation to add this line at the end:
  ``#include <sys/types.h>``

* Run::

      git clone https://bitbucket.org/pypy/numpy.git
      cd numpy
      sudo pypy setup.py install

  or download https://bitbucket.org/pypy/numpy/get/pypy-compat.zip,
  extract it, and run the last line above.

* If you get a permission error when importing NumPy, you need to
  import NumPy once as root::

      cd somewhere_else_unrelated
      sudo pypy -c 'import numpy'
