GIL removal proposal
--------------------

Hello everyone.

The topic of the infamous Global Interpreter Lock has been around for a while
in the Python community. There has been various attempts at removing it
(some successful ones, e.g. in Jython or IronPython with the help of the platform)
and some yet to bear fruit, like `gilectomy`_. Since February sprint in Leysin,
we've been on-and-off tackling the topic of GIL removal in the PyPy project.

As of Europython announcement, we're able to run (very simple) programs with GIL-less
PyPy that parallelizes nicely. The remaining 90% (and another 90%) of work
is with putting locks in strategic places so PyPy does not segfault
when you try to do a concurrent access to a data structure.

Since such work would complicate the code base and our day to day work,
we would like to judge the interest on the community and the commercial
PyPy users.

We would like to do it in a following way. We are looking for a contract
with companies (individual donations did not work very well for us in the
past). We put the total cost of doing the work at $50k, out of which we
already have backing for about 1/3. If we can get a $100k contract, we would
make it our priority to deliver before the end of the year.

People asked several questions, so I'll try to answer the technical parts
here.

* What would the plan entail?

We've already done the work on Garbage Collector to allow doing multi
threaded programs in RPython. "all" that's left is adding locks on mutable
data structures everywhere in PyPy codebase. Since it'll significantly complicated
our workflow, we need to see real interest in that topic, backed up by
commercial contracts, otherwise we're not going to do it.

* Why the STM effort did not work out?

STM was a research project that proved that the idea is possible. However,
the amount of user effort that's required to make programs run nicely
parallelizable is both significant and we never managed to develop tools
that would help nicely. At the present time we're not sure if more manpower
spent on tooling would improve the situation or idea is doomed. The whole
approach also ended up being a significant overhead on single threaded programs,
which means that it's very easy to make your programs slower.

* Would subinterpreters not be a better idea?

Python is a very mutable language - there is tons of mutable state and
basic objects that are compile time in other languages, like classes and functions
are mutable at runtime. That means that sharing things between subinterpreters would
be restricted to basic immutable data structures, which defeats the point compared
to multi-processing approach. We don't believe it's a viable approach without
seriously impacting the semantics of the language.

Best regards,
Maciej Fijalkowski
