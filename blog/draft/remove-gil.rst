GIL removal proposal
--------------------

Hello everyone.

Discussions about the infamous Global Interpreter Lock have been around for a while
in the Python community. There has been various attempts at removing it:
some were successful, like e.g. in Jython or IronPython with the help of the platform, and some yet to bear fruit, like `gilectomy`_. Since our `February sprint`_ in Leysin,
we've been on-and-off tackling directly the topic of GIL removal in the PyPy project.
We believe that the work done in IronPython or Jython can be reproduced with
only a bit more effort. Compared to that, removing the GIL in CPython is a much
harder topic, since it also requires tackling the problem of multi-threaded reference
counting. See the section below for further discussions.

.. _`February sprint`: https://morepypy.blogspot.it/2017/03/leysin-winter-sprint-summary.html

As we announced at EuroPython, what we have got so far is a GIL-less PyPy
which can run **very simple** multi-threaded programs which are nicely
parallelized.  At the moment, non-simple programs most likely segfaults: the
remaining 90% (and another 90%) of work is with putting locks in strategic
places so PyPy does not segfault when you try to do concurrent accesses to
data structures.

Since such work would complicate the code base and our day-to-day work,
we would like to judge the interest on the community and the commercial
partners to make it happen (we are not looking for individual
donations at this point).  We estimate a total cost of $50k,
out of which we already have backing for about 1/3 (with a possible 1/3
extra from the STM money, see below).  This would give us a good
shot at delivering a good proof of concept of working PyPy no-GIL. If we can get a $100k
contract, we will deliver a fully working PyPy interpreter with no GIL as a release,
possibly separate from the default PyPy release.

People asked several questions, so I'll try to answer the technical parts
here.

* What would the plan entail?

We've already done the work on Garbage Collector to allow doing multi-
threaded programs in RPython.  "All" that is left is adding locks on mutable
data structures everywhere in the PyPy codebase. Since it'll significantly complicate
our workflow, we need to see real interest in that topic, backed up by
commercial contracts, otherwise we're not going to do it.

* Why the STM effort did not work out?

STM was a research project that proved that the idea is possible. However,
the amount of user effort that is required to make programs run in a
parallelizable way is significant, and we never managed to develop tools
that would help in doing so.  At the moment we're not sure if more manpower
spent on tooling would improve the situation or if the whole idea is really doomed.
The approach also ended up being a significant overhead on single threaded programs,
so in the end it is very easy to make your programs slower.  (We have some money
left in the donation pot for STM which we are not using; according to the rules, we
could declare the STM attempt failed and channel that money towards the present
GIL removal proposal.)

* Would subinterpreters not be a better idea?

Python is a very mutable language - there are tons of mutable state and
basic objects (classes, functions,...) that are compile-time in other
language but runtime and fully mutable in Python.  In the end, sharing
things between subinterpreters would be restricted to basic immutable
data structures, which defeats the point: it has the same problems as
the approach of having multiple processes and no additional benefits.
We believe that this is not viable without seriously impacting the
semantics of the language (a conclusion which applies to many other
approaches too).

* Why is it easier to do in PyPy than CPython?

Removing the GIL in CPython has two problems - how do we guard access to mutable
data structures with locks and what do we do with reference counting that needs
to be guarded. PyPy only has the former problem; the latter doesn't exist,
due to a different garbage collector approach.  Of course the first problem
is a mess too, but at least we are already half-way there. Compared to Jython
or IronPython, PyPy lacks some data structures that are provided by JVM or .NET,
which we would need to implement, hence the problem is a little harder
than on an existing multithreaded platform. However, there is good research
and we know how that problem can be solved.

Best regards,
Maciej Fijalkowski
