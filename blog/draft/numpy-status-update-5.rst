NumPy status update #5
----------------------

Hello.

I'm quite excited to inform that work on NumPy in PyPy has been restarted
and there has been quite a bit of progress on the NumPy front in PyPy in the
past two months. Things that happened:

* **complex dtype support** - thanks to Matti Picus, NumPy on PyPy now supports
  complex dtype (only complex128 so far, there is work on the other part)

* **big refactoring** - probably the biggest issue we did was finishing
  a big refactoring that disabled some speedups (notably lazy computation
  of arrays), but lowered the barrier of implementing cool new features.
  XXX: explain better why removing a speedup is a good thing, maybe?

* **fancy indexing support** - all fancy indexing tricks should now work,
  including ``a[b]`` where ``b`` is an array of integers.

* **newaxis support** - now you can use newaxis features

* **improvements to ``intp``, ``uintp``, ``void``, ``string`` and record dtypes**

Features that have active branches, but hasn't been merged:

* **float16 dtype support**

* **missing ndarray attributes** - this is a branch to finish all attributes
  on ndarray, hence ending one chapter.

* **pickling support for numarray** - hasn't started yet, but next on the list

More importantly, we're getting very close to able to import the python part
of the original numpy with only import modifications and running it's tests.
Most tests will fail at this point, however it'll be a good start for another
chapter :-)

Cheers,
fijal
