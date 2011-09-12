Little things that PyPy makes possible
======================================

PyPy is just a python interpreter. One of the original goals of the project
were to make existing python programs run faster, and PyPy succeeded in that.
However, the even more exciting part is that optimizations implemented in PyPy
let people do things in Python that were not possible before, like real-time
video processing, numeric array manipulation faster than in C etc. etc.

During the talk I'll present some demos and talk what things are possible having
a decent optimizing just-in-time compiler and briefly discuss strategies that
we used for achieving this. I'll also discuss how faster-than-C, pypy's original
goal from years ago, was after all not that far off.
