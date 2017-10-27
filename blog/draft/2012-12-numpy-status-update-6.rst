NumPy status update #6
----------------------

An update, and some good news

First the update:

* **dtype support** - NumPy on PyPy now supports non-native storage formats.
  Due to a lack of true support for longdoubles in rpython, we decided to back
  out the support of longdouble-as-double which was misleading.

* **missing ndarray attributes** - work has been made toward supporting the 
  complete set of attributes
  on ndarrays. We are progressing alphabetically, and have made it to d.
  Unsupported attributes, and unsupported arguments to attribute calls
  will raise a NotImplementedError.

* **pickling support for numarray** - hasn't started yet, but next on the list

* There has been some work on exposing **FFI routines** in numpypy.

* Brian Kearns has made progress in improving the **numpypy namespace**.
  The python numpypy submodules now more closely resemble their numpy 
  counterparts. Also, translated _numpypy submodules are now more properly 
  mapped to the numpy core c-based submodules, furthering the goal of being 
  able to install numpy as a pure-python module with few modifications.

And now the good news:

While our funding drive over 2012 did not reach our goal, we still managed to 
raise a fair amount of money in donations. So far we only managed to spend around $10 000 of it.
We issued a call for additional developers, and are glad to welcome Romain Guillebert and Ronan Lamy
to the numpypy team. Hopefully we will be able to report on speedier progress soon.

Cheers,
Matti Picus, Maciej Fijalkowski
