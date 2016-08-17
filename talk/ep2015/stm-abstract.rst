=========================
The GIL is dead: PyPy-STM
=========================

Abstract
--------

Take a big, non-multithreaded program, and run in on multiple cores!

PyPy, the Python implementation written in Python, experimentally
supports Software Transactional Memory (STM).  It runs without the
Global Interpreter Lock (GIL).

The strength of STM is not only to remove the GIL, but to also enable
a novel use of multithreading, inheritently safe, and more useful in
the general case than other approaches like OpenMP.  The main news
from last year's presentation is that there is now a way to get
reports about the "STM conflicts", which is essential to go past toy
examples.  With it, you can incrementally remove conflicts from large
code bases until you see a benefit from PyPy-STM.  The goal of the
talk is to give several concrete examples of doing that.
