NumPy status update
-------------------

Hello everyone.

It's been a while since we posted a numpy work update, but I'm pleased to
inform you that work on it has been restarted. A lot of the work has been
done by Matti Picus, who is one of the newest contributors to the PyPy
project. None of the work below has been merged so far, it's work in progress:

* Complex dtype support.

* Fixing incompatibilities between numpy and pypy's version.

* Refactoring numpypy to simplify the code and make it easier for new
  contributors.

* Reuse most of the numpy's pure python code without modifications.

Finishing this is also the plan for the next month.

Cheers,
fijal
