How to get the most out of PyPy
===============================

* Why would you use PyPy - a quick look:
  * performance
  * memory consumption
  * numpy (soon)
  * sandbox
* Why you would not use PyPy (yet)
  * embedded
  * some extensions don't work (lxml)
  * but there are ways around it!
* How PyPy Works
  * Bytecode VM
  * GC
    * not refcounting
    * Generational
    * Implications (building large objects)
  * JIT
    * JIT + Python
      * mapdict
      * globals/builtins
    * tracing
    * resops
    * optimizations
* A case study
  * Examples, examples, examples
  * Open source application (TBD)
  * Jitviewer
* Putting it to work
  * Workshop style
