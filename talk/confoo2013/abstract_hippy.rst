
How I created a proof-of-concept PHP interpreter in 2 months.
=============================================================

HipPy is a proof of concept PHP VM developed as a research effort sponsored
by Facebook. Despite only two months of work on it, while not production ready,
it implements enough of the PHP language to run shootout benchmarks, without
compromising PHP semantics. Due to usage of the PyPy translation toolchain
it's also very fast - over 2x faster than hiphop, an optimizing compiler
from PHP to C++ developed by Facebook over years. I would like to present
the simplicity of implementation when using the PyPy toolchain.

NOTES TO ORGANIZERS:

PyPy is not only a python interpreter but also a toolchain for creating dynamic
language virtual machines. In the past we developed a Prolog VM called pyrolog,
a scheme VM and some smaller ones. External people developed a new VM to
the converge language which outperformed the C implementation drastically.
In this talk I'm going to present how much easier it is to use the PyPy
toolchain than implementing the just-in-time compiler by hand in C or C++.
