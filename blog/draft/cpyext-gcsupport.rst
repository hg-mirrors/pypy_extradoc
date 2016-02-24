CAPI Support update
===================

I have merged a rewrite of the interaction between c-API c-level objects and 
interpreter level objects. Each refcounted c-level object is now reflected in
an interpreter level object, and the garbage collector can release the object
pair only if the refcount is 0 and the interpreter level object is not longer
referenced.

The rewrite significantly simplifies our previous code, and should make using
the c-API less slow (it is still slower than using pure python though).
XXX citations needed ...

The good news is that now PyPy can support the upstream `lxml`_ package, which is
is one of the most popular packages on PyPI (specifically version X.X.X with old
PyPy specific hacks removed). We do recommend using the `cffi lxml`_ alternative,
since it will be faster on PyPy.

We are actively working on extending our c-API support, and hope to soon merge
a branch to support more of the c-API functions. Please try it out and let us
know how it works for you.

Armin Rigo and the PyPy team
