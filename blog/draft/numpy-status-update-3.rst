NumPy on PyPy progress report
=============================

Hello.

A lot of things happened in March, like `pycon`_. I was also busy doing other
things (pictured), so apologies for the late numpy status update.

However, a lot of things have happened and numpy continues to be on of the
main points of entry for hacking on PyPy. Apologies to all the people who's
patches I don't review in timely manner, but seriously, you do **a lot** of
work.

The list of things is definitely not exhaustive, and I might be forgetting
important contributions. In a loose order:

* Matti Picus made ``out`` parameter working for a lot (but not all)
  functions.

* We merged record dtypes support. The only missing dtypes left are complex
  (important), datetime (less important) and object (which will probably
  never be implemented).

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

  +

Next step would be to just continue implementing missing features. Future
is hard to predict, but we're not far off!

.. _`pycon`: http://us.pycon.org
