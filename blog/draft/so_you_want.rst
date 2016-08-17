So you want to try PyPy?
------------------------

Hello.

During the PyCon trip multiple people asked me how exactly they could run
their stuff on PyPy to get the speedups. Now, in an ideal world,
you would just swap CPython with PyPy, everything would run tons of times
faster and everyone would live happily ever after. However, we don't live in
an ideal world and PyPy does not speed up *everything* you could
potentially run. Chances are that you can run your stuff quite a bit faster, but
it requires quite a bit more R&D than just that. This blog post is an attempt to
explain certain steps that might help. So here we go:

* Download and install PyPy. 2.0 beta 1 or upcoming 2.0 beta 2 would be a good
  candidate; it's not called a beta for stability reasons.

* Run your tests on PyPy. There is absolutely no need for fast software that
  does not work. There might be some failures. Usually they're harmless (e.g. 
  you forgot to close the file); either fix them or at least inspect them. In
  short, make sure stuff works.

* Inspect your stack. In particular, C extensions, while sometimes working, are
  a potential source of instability and slowness. Fortunately,
  since the introduction of `cffi`_, the ecosystem of PyPy-compatible software
  has been growing. Things I know are written with PyPy in mind:

  * the new version of `pyOpenSSL`_ will support PyPy via cffi

  * `psycopg2cffi`_ is the most actively maintained postgres binding for PyPy,
    with pg8000 reported working

  * mysql has a `ctypes based implementation`_ (although a cffi-based one would
    be definitely better)

  * PyPy 2.0 beta 2 will come with sqlite-using-cffi

  * `lxml-cffi`_

  * `uWSGI`_, while working, is almost certainly not the best choice. Try
    `tornado`_, `twisted.web`_, `cyclone.io`_, `gunicorn`_ or `gevent`_
    (note: gevent support for PyPy is not quite finished; will write about it
    in a separate blog post, but you can't just use the main branch of gevent)

  * consult (and contribute to) `pypy compatibility wiki`_ for details (note
    that it's community maintained, might be out of date)

.. _`pypy compatibility wiki`: https://bitbucket.org/pypy/compatibility/wiki/Home
.. _`cffi`: http://cffi.readthedocs.org
.. _`pyOpenSSL`: https://launchpad.net/pyopenssl
.. _`psycopg2cffi`: https://github.com/chtd/psycopg2cffi
.. _`ctypes based implementation`: https://github.com/quora/mysql-ctypes
.. _`lxml-cffi`: https://github.com/amauryfa/lxml/tree/lxml-cffi
.. _`uWSGI`: https://github.com/unbit/uwsgi-docs
.. _`tornado`: http://www.tornadoweb.org/en/stable/
.. _`twisted.web`: http://twistedmatrix.com/trac/wiki/TwistedWeb
.. _`cyclone.io`: http://cyclone.io/
.. _`gunicorn`: http://gunicorn.org/
.. _`gevent`: http://www.gevent.org/

* Have benchmarks. If you don't have benchmarks, then performance does not
  matter for you. Since PyPy's warm-up time is bad (and yes, we know, we're
  working on it), you should leave ample time for warm-ups. Five to ten seconds
  of continuous computation should be enough.

* Try them. If you get lucky, the next step might be to deploy and be happy.
  If you're unlucky, profile and try to isolate bottlenecks. They might be in
  a specific library or they might be in your code. The better you can isolate 
  them, the higher your chances of understanding what's going on.

* Don't take it for granted. PyPy's JIT is very good, but there is a variety
  of reasons that it might not work how you expect it to. A lot of times it 
  starts off slow, but a little optimization can improve the speed as much as 
  10x. Since PyPy's runtime is less mature than CPython, there are higher 
  chances of finding an obscure corner of the standard library that might be
  atrociously slow.

* Most importantly, if you run out of options and you have a reproducible
  example, **please report it**. A `pypy-dev`_ email, popping into ``#pypy``
  on ``irc.freenode.net``, or getting hold of me on twitter are good ways.
  You can also contact me directly at *fijall at gmail.com* as well. While
  it's cool if the example is slow, a lot of problems only show up on large
  and convoluted examples. As long as I can reproduce it on my machine or I can
  log in somewhere, I am usually happy to help.

* I typically use a combination of `jitviewer`_, `valgrind`_ and
  `lsprofcalltree`_ to try to guess what's going on. These tools are all
  useful, but use them with care. They usually require quite a bit of 
  understanding before being useful. Also sometimes they're just plain useless
  and you need to write your own analysis.

I hope this summary of steps to take is useful. We hear a lot of stories
of people trying PyPy, most of them positive, but some of them negative.
If you just post "PyPy didn't work for me" on your blog, that's
cool too, but you're missing an opportunity. The reasons may vary from
something serious like "this is a bad pattern for PyPy GC" to something
completely hilarious like "oh, I left this ``sys._getframe()`` somewhere
in my hot loops for debugging" or "I used the ``logging`` module which uses
``sys._getframe()`` all over  the place".

Cheers,
fijal

.. _`pypy-dev`: http://mail.python.org/mailman/listinfo/pypy-dev
.. _`jitviewer`: https://bitbucket.org/pypy/jitviewer
.. _`valgrind`: http://valgrind.org/
.. _`lsprofcalltree`: https://bitbucket.org/pypy/pypy/src/default/rpython/tool/lsprofcalltree.py?at=default
