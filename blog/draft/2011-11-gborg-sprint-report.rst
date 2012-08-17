Gothenburg sprint report
=========================

In the past week, we have been busy hacking on PyPy at the Gothenburg sprint,
the second of this 2011.  The sprint was hold at Laura's and Jacob's place,
and here is a brief report of what happened.

.. img:: 5x-cake.jpg

In the first day we welcomed Mark Pearse, which was new to PyPy and at his
first sprint.  Mark worked the whole sprint at the new SpecialisedTuple_
branch, whose aim is to have a special implementation for small 2-items and
3-items tuples of primitive types (e.g., ints or floats) to save memory.  Mark
paired with Antonio for a couple of days, then he continued alone and did amazing
job.  He even learned how to properly do Test Driven Development :-).

.. _SpecialisedTuple: http://bitbucket.org/pypy/pypy/changesets/tip/branch%28%22SpecialisedTuples%22%29

Antonio spent a couple of days investingating whether it is possible to use
`application checkpoint` libraries such as BLCR_ and DMTCP_ to save the state of
the PyPy interpreter between subsequent runs, thus saving also the
JIT-compiled code to reduce the warmup time.  The conclusion is that these are
interesting technologies, but more work would be needed (either on the PyPy
side or on the checkpoint library side) before it can have a practical usage
for PyPy users.

.. _`application checkpoint`: http://en.wikipedia.org/wiki/Application_checkpointing
.. _BLCR: http://ftg.lbl.gov/projects/CheckpointRestart/
.. _DMTCP: http://dmtcp.sourceforge.net/

Then, Antonio spent most of the sprint working on his ffistruct_ branch, whose
aim is to provide a very JIT-friendly way to interact with C structures, and
eventually implement ``ctypes.Structure`` on top of that.  The "cool part" of
the branch is already done, and the JIT already can compile set/get of fields
into a single fast assembly instruction, about 400 times faster than the
corresponding ctypes code.  What is still left to do is to add a nicer syntax
(which is easy) and to implement all the ctypes peculiarities (which is
tedious, at best :-)).

.. _ffistruct: http://bitbucket.org/pypy/pypy/changesets/tip/branch(%22ffistruct%22)

As usual, Armin did tons of different stuff, including fixing a JIT bug,
improving the performance of ``file.readlines()`` and working on the STM_
branch (for Software Transactional Memory), which is now able to run RPython
multithreaded programs using software transaction (as long as they don't fill
up all the memory, because support for the GC is still missing :-)).  Finally,
he worked on improving the Windows version of PyPy, and while doing so he
discovered toghether with Anto a terrible bug which leaded to a continuous
leak of stack space because the JIT called some functions using the wrong
calling convention.

.. _STM: http://bitbucket.org/pypy/pypy/changesets/tip/branch("stm")

Håkan, with some help from Armin, worked on the `jit-targets`_ branch, whose goal
is to heavily refactor the way the traces are internally represented by the
JIT, so that in the end we can produce (even :-)) better code than what we do
nowadays.  More details in this mail_.

.. _`jit-targets`: http://bitbucket.org/pypy/pypy/changesets/tip/branch("stm")
.. _mail: http://mail.python.org/pipermail/pypy-dev/2011-November/008728.html


Andrew Dalke worked on a way to integrate PyPy with FORTRAN libraries, and in
particular the ones which are wrapped by Numpy and Scipy: in doing so, he
wrote f2pypy_, which is similar to the existing ``f2py`` but instead of
producing a CPython extension module it produces a pure python modules based
on ``ctypes``.  More work is needed before it can be considered complete, but
``f2pypy`` is already able to produce a wrapper for BLAS which passes most of
the tests under CPython, although there's still work left to get it working
for PyPy.

.. _f2pypy: http://bitbucket.org/pypy/f2pypy

Christian Tismer worked the whole sprint on the branch to make PyPy compatible
with Windows 64 bit.  This needs a lot of work because a lot of PyPy is
written under the assumption than assumption that the ``long`` type in C has
the same bit size than ``void*``, which is not true on Win64.  Christian says
that in the past Genova-Pegli sprint he completed 90% of the work, and in this
sprint he did the other 90% of the work.  Obviously, what is left to complete
the task is the third 90% :-).  More seriously, he estimated a total of 2-4
person-weeks of work to finish it.

But, all in all, the best part of the sprint has been the cake that Laura
cooked to celebrate the "5x faster than CPython" achievement. Well, actually
our speed_ page reports "only" 4.7x, but that's because in the meantime we
switched from comparing against CPython 2.6 to comparing against CPython 2.7,
which is slightly faster.  We are confident that we will reach the 5x goal
again, and that will be the perfect excuse to eat another cake :-)

.. _speed: http://speed.pypy.org/

