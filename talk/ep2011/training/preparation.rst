================================
PyPy training session
================================

You are encouraged to bring your laptop to the training session.

Make sure that the following prerequisites are met:

  * Install PyPy 1.5:

    - http://pypy.org/download.html

    - http://doc.pypy.org/en/latest/getting-started.html#installing-pypy

  * Make sure that ``setuptools`` or ``distribute`` are installed (look at the
    URL above for instructions)

  * Clone the pypy repository, and update to the 1.5 version::

    $ hg clone http://bitbucket.org/pypy/pypy

    $ cd pypy

    $ hg up -r release-1.5

  * Clone the jitviewer repository and install it on pypy::

    $ hg clone http://bitbucket.org/pypy/jitviewer
    
    $ cd jitviewer

    $ /path/to/pypy-1.5/bin/pypy setup.py develop

  * Download the source code which will be used during the session:

    - http://wyvern.cs.uni-duesseldorf.de/~antocuni/ep2011-training.zip

If you intend to follow also the second part ("Write your own interpreter with
PyPy"), you need to make sure you have a working developing environment:
http://doc.pypy.org/en/latest/getting-started-python.html#translating-the-pypy-python-interpreter

