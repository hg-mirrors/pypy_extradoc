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
  * Open source application (TBD)
  * Tracebin or jitviewer
* Putting it to work
  * Workshop style
