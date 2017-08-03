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

Best regards,
Maciej Fijalkowski
