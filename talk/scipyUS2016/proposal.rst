PyPy and the Numpy/Scipy Stack
==============================

Abstract (500 words or less)
____________________________

PyPy is used successfully in the world of web servers and text processing. 
What can it do for data crunching? How can it possibly work with Numpy and the
rest of the Scientific Python data stack? In this talk I will briefly survey
what is PyPy, our two approaches to compatibility with Numpy, and what that
means for those who are looking for a drop-in solution to their processing
challenges. 

Longer Description
__________________

PyPy is maturing as a drop-in replacement for python 2.7. In the world
of web servers and text processing, PyPy's speed on long-running processes
and compatibility with pure python packages makes it a good fit for mature
technologies looking for a quick speed increase. 

What about the world of number crunching, can PyPy possibly contribute
anything to the crowded field of ahead-of-time solutions like cython or
other just-in-time solutions like Numba? The PyPy team feels very strongly
that we can, and in this talk I will try to outline PyPy's approach to
intgrating numpy and the SciPy stack on top of this alternative interpreter,
after a brief introduction of the RPython toolchain and the PyPy interpreter.

We have been working for a number of years on an alternative 
implementation of the ndarray, tightly integrated to the PyPy machinary.
Reimplementing numpy completely comes with costs, like a constant need to
replicate updates when a new version of numpy is released.
We've been recently experimenting with reusing
more of C numpy through the C API and we have ideas how to merge both 
approaches to have the best of both worlds. 

