Tornado without a GIL on PyPy STM
=================================

Python has a GIL, right? Not quite - PyPy STM is a python implementation
without a GIL, so it can scale CPU-bound work to several cores.
PyPy STM is developed by Armin Rigo and Remi Meier,
and supported by community `donations <http://pypy.org/tmdonate2.html>`_.
You can read more about it in the
`docs <http://pypy.readthedocs.org/en/latest/stm.html>`_.

Although PyPy STM is still a work in progress, in many cases it can already
run CPU-bound code faster than regular PyPy, when using multiple cores.
Here we will see how to slightly modify Tornado IO loop to use
`transaction <https://bitbucket.org/pypy/pypy/raw/stmgc-c7/lib_pypy/transaction.py>`_
module.
This module is `descibed <http://pypy.readthedocs.org/en/latest/stm.html#atomic-sections-transactions-etc-a-better-way-to-write-parallel-programs>`_
in the docs and is really simple to use - please see an example there.
An event loop of Tornado, or any other asynchronous
web server, looks like this (with some simplifications)::

    while True:
        for callback in list(self._callbacks):
            self._run_callback(callback)
        event_pairs = self._impl.poll()
        self._events.update(event_pairs)
        while self._events:
            fd, events = self._events.popitem()
            handler = self._handlers[fd]
            self._handle_event(fd, handler, events)

We get IO events, and run handlers for all of them, these handlers can
also register new callbacks, which we run too. When using such a framework,
it is very nice to have a guaranty that all handlers are run serially,
so you do not have to put any locks. This is an ideal case for the
transaction module - it gives us guaranties that things appear
to be run serially, so in user code we do not need any locks. We just
need to change the code above to something like::

    while True:
        for callback in list(self._callbacks):
            transaction.add(
            self._run_callback, callback)   # added
        transaction.run()                   # added
        event_pairs = self._impl.poll()
        self._events.update(event_pairs)
        while self._events:
            fd, events = self._events.popitem()
            handler = self._handlers[fd]
            transaction.add(                # added
                self._handle_event, fd, handler, events)
        transaction.run()                   # added

The actual commit is
`here <https://github.com/lopuhin/tornado/commit/246c5e71ce8792b20c56049cf2e3eff192a01b20>`_,
- we had to extract a little function to run the callback.

Now we need a simple benchmark, lets start with
`this <https://bitbucket.org/kostialopuhin/tornado-stm-bench/src/a038bf99de718ae97449607f944cecab1a5ae104/primes.py?at=default>`_
- just calculate a list of primes up to the given number, and return it
as JSON::

    def is_prime(n):
        for i in xrange(2, n):
            if n % i == 0:
                return False
        return True

    class MainHandler(tornado.web.RequestHandler):
        def get(self, num):
            num = int(num)
            primes = [n for n in xrange(2, num + 1) if is_prime(n)]
            self.write(json.dumps({'primes': primes}))


We can benchmark it with ``siege``::

    siege -c 50 -t 20s http://localhost:8888/10000

But this does not scale. The CPU load is at 101-104 %, and we handle 30 %
less request per second. The reason for the slowdown is STM overhead,
which needs to keep track of all writes and reads in order to detect conflicts.
And the reason for using only one core is, obviously, conflicts!
Fortunately, we can see what this conflicts are, if we run code like this
(here 4 is the number of cores to use)::

    PYPYSTM=stm.log ./primes.py 4

Than we can use `print_stm_log.py <https://bitbucket.org/pypy/pypy/raw/stmgc-c7/pypy/stm/print_stm_log.py>`_
to analyse this log. It lists the most expensive conflicts::

    14.793s lost in aborts, 0.000s paused (1258x STM_CONTENTION_INEVITABLE)
    File "/home/ubuntu/tornado-stm/tornado/tornado/httpserver.py", line 455, in __init__
        self._start_time = time.time()
    File "/home/ubuntu/tornado-stm/tornado/tornado/httpserver.py", line 455, in __init__
        self._start_time = time.time()
    ...

There are only three kinds of conflicts, they are described in
`stm source <https://bitbucket.org/pypy/pypy/src/6355617bf9a2a0fa8b74ae17906e4a591b38e2b5/rpython/translator/stm/src_stm/stm/contention.c?at=stmgc-c7>`_,
Here we see that two threads call into external function to get current time,
and we can not rollback any of them, so one of them must wait till the other
transaction finishes.
For now we can hack around this by disabling this timing - this is only
needed for internal profiling in tornado.

If we do it, we get the following results:

============  =========
Impl.           req/s
============  =========
PyPy 2.4        14.4
------------  ---------
CPython 2.7      3.2
------------  ---------
PyPy-STM 1       9.3
------------  ---------
PyPy-STM 2      16.4
------------  ---------
PyPy-STM 3      20.4
------------  ---------
PyPy STM 4      24.2
============  =========

As we can see, in this benchmark PyPy STM using just two cores
can beat regular PyPy!
This is not linear scaling, there are still conflicts left, and this
is a very simple example but still, it works! And it was easy!

Although it is definitely not ready for production use, you can already try
to run things, report bugs, and see what is missing in user-facing tools
and libraries.

Benchmark setup:

* Amazon c3.xlarge (4 cores) running Ubuntu 14.04
* pypy-c-r74011-stm-jit
* http://bitbucket.org/kostialopuhin/tornado-stm-bench at a038bf9
* for PyPy-STM in this test the variation is higher,
  best results after warmup are given

