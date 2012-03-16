PyPy JIT under the hood
=======================

PyPy is probably the fastest Python implementation around, thanks to its
automatically generated JIT compiler.  This talk explains how the JIT works
internally: in particular, it shows all the intermediate steps which lead to
the compilation of the Python source into fast machine code, and how to use
the right tools to inspect the output of the JIT compiler.

By examining the internals of the JIT, you will also learn why some code is
more "JIT friendly" than other, and how to write programs which exploits its
full potential.

