
How I created a proof-of-concept PHP interpreter in 2 months.
=============================================================

HipPy is a proof of concept PHP VM developed as a research effort sponsored
by Facebook using PyPy. After two months, while not production ready,
it implements enough of the PHP language to run shootout benchmarks, without
compromising PHP semantics. It's also very fast - over 2x faster than hiphop,
a compiler from PHP to C++ developed by Facebook.

NOTES TO ORGANIZERS:

PyPy is not only a python interpreter but also a toolchain for creating dynamic
language virtual machines. In the past we developed a Prolog VM,
a scheme VM and some others. Laurence Tratt developed a new VM for
the converge language which outperformed the C implementation.
I'm going to present how easy it is to use PyPy than implementing a VM
by hand.

