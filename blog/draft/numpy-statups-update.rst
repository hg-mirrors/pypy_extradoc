NumPy Status Update
-------------------

Hi everyone,

It's been a little while since we wrote about NumPy on PyPy, so I wanted to
give everyone an update on what we've been up to, and what's up next for us.

Some of the things that have happened since last we wrote are:

* We added ``dtype`` support, meaning you can now create arrays of a bunch of
  different types, including bools, ints of a various sizes, and floats.
* More array methods and ufuncs, including things like comparison methods
  (``==``, ``>``, etc.)
* Support for more and more argument types, for example you can index by a
  tuple now (only works with tuples of length one, since we only have
  single-dimension arrays thus far).

Some of the things we're working on at the moment:

* More dtypes, including unsigned integers, singe floats, and complex doubles.
* Subscripting arrays by other array as indices, and by bool arrays as masks.
* Starting to reuse python-level original numpy

Some of the things on the near horizon are:

* Better support for scalar data, for example did you know that
  ``numpy.array([True], dtype=bool)[0]`` doesn't return a ``bool`` object?
  Instead it returns a ``numpy.bool_``.
* Multi-dimensional array support.

If you're interested in helping out, we always love more contributors,
Alex, Maciej, Justin, and the whole PyPy team
