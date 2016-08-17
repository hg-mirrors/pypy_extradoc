NumPy on PyPy progress report
=============================

Hello.

A lot of things happened in March, like `pycon`_. I was also busy doing other
things (pictured), so apologies for the late numpy status update.

However, a lot of things have happened and numpy continues to be one of the
main points of entry for hacking on PyPy. Apologies to all the people whose
patches I don't review in timely manner, but seriously, you do **a lot** of
work.

This list of changes is definitely not exhaustive, and I might be forgetting
important contributions. In a loose order:

* Matti Picus made ``out`` parameter work for a lot of (but not all)
  functions.

* We merged record dtypes support. The only missing dtypes left are complex
  (important), datetime (less important) and object (which will probably
  never be implemented because XXXXXXX).

* Taavi Burns and others implemented lots of details, including lots of ufuncs.
  On the completely unscientific measure of "implemented functions" on
  `numpypy status page`_, we're close to 50% of numpy working. In reality
  it might be more or less, but after complex dtypes we're getting very close
  to running real programs.

* Bool indexing of arrays of the same size should work, leaving only
  arrays-of-ints indexing as the last missing element of fancy indexing.

* I did some very early experiments on SSE. This work is **seriously**
  preliminary - in fact the only implemented operation is addition of
  float single-dimension numpy arrays. However, results are encouraging,
  given that our assembler generator is far from ideal:

  +---------------+----------+----------+------+----------------+------------+
  |               | Numpy    | PyPy SSE | PyPy | GCC non-looped | GCC looped |
  +---------------+----------+----------+------+----------------+------------+
  | ``a+b``       | 0.6s     | 0.3s     | 0.4s | 0.3s           | 0.25s      |
  +---------------+----------+----------+------+----------------+------------+
  | ``a+b+c``     | 1.9s     | 0.35s    | 0.5s | 0.7s           | 0.32s      |
  +---------------+----------+----------+------+----------------+------------+
  | ``a+b+c+d+e`` | 3.2s     | 0.36s    | 0.8s | 1.7s           | 0.51s      |
  +---------------+----------+----------+------+----------------+------------+

  The `benchmark repo`_ is available. GCC was run with ``-O3``, no further
  options specified. PyPy was run with default options, the SSE branch is under
  ``backend-vector-ops``, but **it's not working completely** yet.

  One might argue that C and Python is not the same code - indeed it is not.
  It just shows some possible approach to writing numeric code.

Next step would be to just continue implementing missing features such as

* specialised arrays i.e. masked arrays and matrixes

* core modules such as ``fft``, ``linalg``, ``random``.  

* numpy's testing framework

The future is hard to predict, but we're not far off!

.. _`pycon`: http://us.pycon.org
.. _`numpypy status page`: http://buildbot.pypy.org/numpy-status/latest.html
.. _`benchmark repo`: https://bitbucket.org/fijal/hack2/src/fa3119d8ade6/bench/numeric
