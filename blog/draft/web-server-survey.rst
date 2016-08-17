
Hello everyone.

This is a small survey of performance of various wsgi servers available
under CPython and PyPy. Note that while this is of high interest to me, since
it stressed the underlaying runtime quite a lot, there is a high chance
the underlaying web server really does not matter all that much for the
performance of your application. **Measure** first if the web server is
actually the problem.

The actual benchmark consists of sending a `relatively complex HTTP query`_
(which is roughly what chrome sends by default if issuing a GET) and
then awaiting response without keeping the connection alive. I wrote
a very crude `benchmarking tool`_ and I would not recommend anyone using it.
In principle, it's broken and assumes fragmentation of packages that happened
to happen on my test machine, but will not happen in the wild. I suggest use
`locust.io`_ or similar. The benchmarks can be found inside
`asynchammer's repository`_. Note that this is precisely a benchmark of
pure (or mostly in case of gevent) Python web servers. In this stupid benchmark,
if you run uWSGI and CPython, it'll be faster, because there is no Python code
involved (it just really executes one function). If you want to benchmark
a full web application, you should do just that and not only a server.

The benchmarks were run like that::

   python asynchammer.py --workers=4 --max=120000 --warmup=30000 --host=localhost:<port>

Using pypy. The servers were run either ``python`` ``example name`` or
``gunicorn -w 1 gunicorn_example:app``. In all cases the newest released
versions as of today were used, except gevent where a recent git clone
was used of gevent 1.0. Additionally PyPy version used `pypycore`_ for the
gevent loop. You run it like this:
``GEVENT_LOOP=pypycore.loop pypy gevent_example.py`` assuming everything is on
path. PyPy 2.0 beta 2 was used vs CPython 2.7.3.

What this benchmark does?
-------------------------

We issue 120k requests on a machine that has enough cores (and dies) to run
client and server relatively separated (there is no cache sharing between dies).
First 30k is discarded, in order to warm up the JIT, both on the client and
on the server side.
The requests are issued 10 at once (for each of the 4 workers) and then when
a request finishes, a new one is issued. The workers max out at around 11k req/s
which is what I could get out of apache serving static files. That amount of
load makes 2 apache processes run at around 150% CPU time each. All python
servers were run in a single process. I did run benchmark multiple times
to make sure that the results are at least roughly reproducible, but I did
not run any formal statistics.

How relevant are those results for me?
--------------------------------------

If you're looking for a website performance enhancements, unlikely they're
any relevant. If you're getting (say) 500 req/s from a single worker on your
website, then the web server consumes less than 25% of the time. If you're
seeing numbers in thousands per second than very relevant. If you don't happen
to have benchmarks, then it really doesn't matter.

CPython:

twisted.web: 2300
cyclone.io: 2400
tornado: 3200
gunicorn (sync): 3700
gevent: 4100
eventlet: 3200

PyPy:

twisted.web: 8300
cyclone: 7400
tornado: 7600
gunicorn (sync): 6900
gevent: 6400
eventlet: 6700

Giveaways
---------

There are a few obvious results. One is that parsing HTTP headers is quite
a bit of work. PyPy does some work there, but looking at traces it can clearly
be improved. Expect some work in that area. Another one is that an actual
choice of the web server does not quite matter what you choose (as long as it's
running under PyPy :)). Note that the difference here
is that we used a relatively real-life example of HTTP headers, as opposed
to ``ab`` which uses a very simple one. In the case of simple HTTP headers,
it matters more and you get drastically different results, which I'm not going
to publish because I claim they're even less relevant.

It also looks like the choice for CPython and the choice for PyPy are quite
drastically different, with work from twisted folks helping us a lot, while
with CPython "running a loop in C" is still very important.

To summarize, it seems that Python, and especially PyPy, is quite fast.
With 11k req/s, apache is running at around 300% CPU in total,
while none of the examples run above 120% CPU, which is normal CPU +
loopback costs. uWSGI in my benchmarks also scored

I hope this will be one of the series of articles about
"how to compose a fast web stack using PyPy", but who knows what future holds.

Cheers,
fijal
