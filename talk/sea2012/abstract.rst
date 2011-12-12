Fast numeric in Python - NumPy and PyPy
=======================================

Python has seen a growing adoption as a new scientific processing language
in the past few years. It has been successfully used as a glue language
to drive various simulations implemented in either C, Fortran or the array
manipulation language implemented in the NumPy package. Originally the main
reason why Python was used only as a glue language is because the original
Python implementation is relatively slow. With the recent progress in the PyPy
project, it has been shown that while still not at C speeds, it has been
gaining significant performance improvements the releases, bringing it
closer and closer to C-level speeds. In this talk I would like to explore
how to use it right now, in the near future and our plans to provide a very
robust infrastructure for implementing numerical computations. I will also
spend some time exploring the ideas how dynamic compilation can eventually
outperform static compilation and how having a high-level language helps here.
