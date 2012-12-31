NumPy status update #6
----------------------

Hello.

This is the last two months update of the activities on the NumPyPy project.

First the update:

* **dtype support** - NumPy on PyPy now supports all the numeric dtypes in numpy,
  including non-native storage formats, longdouble, clongdouble and friends.

* **missing ndarray attributes** - work has been made toward supporting the attributes
  on ndarrays. We are progressing alphabetically, and have made it to d.

* **pickling support for numarray** - hasn't started yet, but next on the list

* There has been some work on exposing FFT routines into numpypy.

More importantly, we're closing on being able to run the pure-python part of
numpy without modifications. This is not getting us close to passing all
the tests, but it's a good start.

The most important part is the funding. While we managed to get a significant
amount of money in donations, we only managed to spend around $10 000 from it
so far. XXX

Cheers,
Matti Picus, Maciej Fijalkowski
