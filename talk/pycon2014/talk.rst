The status of PyPy
==================

PyPy is an alternative Python interpreter.  It is seriously fast, but
progress purely in that direction is reaching limits.  Instead, it is
growing support for a larger part of the Python ecosystem: a long list
of common libraries are going from "unsupported" to "badly supported" to
"well supported".  We also have beta Python 3 support.  In short, try
PyPy today :-)

On the research front, Transactional Memory seems to work as a way to
run programs on multiple cores.  It is coming along, fully integrated
with the JIT compiler.  We will show various examples, including
versions of event libraries (like Twisted, Tornado, greenlet...) that
run existing non-multithreaded programs on multiple cores.
