How to install NumPy on PyPy
============================

* apt-get install pypy-dev

* Windows: you need to edit the Python.h from PyPy to add at the end:
  ``#include <sys/types.h>``

* git clone https://bitbucket.org/pypy/numpy.git; cd numpy;
  sudo pypy setup.py install

* sudo pypy -c 'import numpy'       # only once
