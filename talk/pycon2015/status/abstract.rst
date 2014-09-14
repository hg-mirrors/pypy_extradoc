Pycon 2015 proposal for PyPy status

Title
-----

PyPy - the last 2 years of progress

Category
--------

Implementations, Virtual Machines

Duration
--------

30min

Description (one paragraph, 400 chars max)
------------------------------------------

This talk describes what happened in the PyPy ecosystem in the last 2 years, a
timeframe in which PyPy has been successfully deployed multiple times while
yielding interesting performance improvements and a timeframe in which more
libraries started being compatible with PyPy through the use of cffi.

Audience
--------

Regular Python programmers interested in performance,
looking to learn more about PyPy. No virtual machine knowledge necessary

Python level
------------

Medium

Objectives
----------

We want to explain what we have done during the two years between our talks
at Pycon and how we expanded PyPy community and the ability to use PyPy
in various contexts.

Detailed Abstract
-----------------

PyPy has been in the works for more than ten years and has reached relative
maturity with more and more libraries working under PyPy and more deployments
happening. Right now it entertains between 0.5-1.0% of PyPI package downloads
(with CPython taking virtually all of the rest), used mostly for
high-performance web servers.

Since no PyPy talk happened at PyCon 2014, we would like to present what
we have achieved during the two years between talks. We would like to cover
advancements in the PyPy performance landscape, but more importantly how
we're addresssing the community needs and building the ecosystem. These days
a lot of libraries that used to bind to C using the CPython C API are either
using cffi or have alternatives using cffi.

We would also like to walk through a few success stories that we have
experienced. Unfortunately the biggest chunk of PyPy clients are very
secretive (e.g. trading companies), but we can still present a few case studies.

Outline
-------

It's really hard to come up with the outline given the time to Pycon. We'll
definitely talk about cffi and the community, but the exact extend
will be decided later.

Additional notes
----------------

Long-time PyPy speaker at numerous conferences (PyCon, EuroPython, etc.)
