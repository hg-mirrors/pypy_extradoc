NumPy status update #6
----------------------

Hello.
Over the past two months we have made progress, and would like to request your help.

First the update:
* **dtype support** - NumPy on PyPy now supports all the numeric dtypes in numpy,
  including non-native storage formats, longdouble, clongdouble and friends.

* **missing ndarray attributes** - work has been made toward supporting the attributes
  on ndarrays. We are progressing alphabetically, and have made it to d.

* **pickling support for numarray** - hasn't started yet, but next on the list

More importantly, we're getting very close to be able to import the python part
of the original numpy with only import modifications, and running its tests.
Most tests will fail at this point, however it'll be a good start for another
chapter :-)


Numpy in pypy could use your help, in spite of the generous donations we have not been
able to move forward as fast as we wish. Please
get involved by trying it out, picking a feature that you would love to have, and
helping us get that feature implemented.

Cheers,
Matti Picus
