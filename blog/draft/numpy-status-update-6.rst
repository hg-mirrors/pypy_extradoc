NumPy status update #6
----------------------

This is status report on PyPy's NumPyPy project.

First the update:

* **dtype support** - NumPy on PyPy now supports all the numeric dtypes in numpy,
  including non-native storage formats, longdouble, clongdouble and friends.

* **missing ndarray attributes** - work has been made toward supporting the 
  complete set of attributes
  on ndarrays. We are progressing alphabetically, and have made it to d.
  Unsupported attributes, and unsupported arguments to attribute calls
  will raise a NotImplementedException.

* **pickling support for numarray** - hasn't started yet, but next on the list

* There has been some work on exposing FFI routines in numpypy.

More importantly, we're closing on being able to run the pure-python part of
numpy without modifications. This is not getting us close to passing all
the tests, but it's a good start.

The most important part is the funding. While we managed to get a significant
amount of money in donations, we only managed to spend around $10 000 from it
so far. We have issued a call for additional developers, and hope to be able to
report on speedier progress soon.

Cheers,
Matti Picus, Maciej Fijalkowski
