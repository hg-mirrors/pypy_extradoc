NumPy Update
============

Executive summary: If you wish to try out numpy on pypy, the way to do it is
changing. ``import numpy`` will no longer work out-of-the-box, you will have to
install a hacked numpy package.

The way it was
--------------

PyPy implements a builtin module called _numpypy that exports a native ndarray,
dtype, ufunc, and some other helpers. The current status of the trunk can be
viewed on the _`numpy status page`. There was a file numpy.py located in the
sys.path that wrapped the _numpypy module to look like numpy's extension (compiled
c) modules. So you could download a pypy.tgz, open it up, and do ``import numpy``
which would emit a warning, but provide some of the numpy functionality.

What came next
------------

As we become more and more numpy-compatible, we find ourselves copying files
from numpy into the pypy source code tree, to provide app-level support. Things
like numpy.eye, numpy.identity, and all the module level funcitons that simply
create an ndarray and then call the corresponding method on the ndarray.

Since that seems repetative and prone to bitrot, we began a _`fork of numpy`
to allow mortals to run ``setup.py install`` and get much more of numpy working.

What went wrong, choices, and the decision
---------------------------------

The numpy.py file masks the numpy package installed in site-packages since it
appears first on the search path. So we could have hacked at it to import numpy
if such a package exists and to export it anew. But the better choice was
made - to remove it entirely.

What the future holds
--------------------

PyPy is making great progress, the engine is getting better and better, and
interfacing to packages is getting easier. Currently, using the pypy-hack 
branch of  the _`fork of numpy`
and another _`fork of matplotlib`, you can create plots and save them to files.
These extensions use the immature and slow c api (cpyext) in PyPy. We would
prefer to use the jit-friendly cffi for extension modules, progress has been
made writing a cffi interface for wxWidgets in a GSOC, but _`that` is a subject
for another post. We will soon be uploading the PyPy compatible numpy package
to _`PyPi`, and would love to get more people involved in hacking, testing,
and benchmarking numpy on PyPy.

Matti (mattip), and the PyPy team

.. _`numpy status page`: http://buildbot.pypy.org/numpy-status/latest.html
.. _`fork of numpy`: https://github.com/mattip/numpy
.. _`fork of matplotlib`: https://github.com/mattip/matplotlib
.. _`that`: http://waedt.blogspot.co.il
