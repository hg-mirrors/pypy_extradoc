Status since last EuroPython
----------------------------

* 4 releases since last EuroPython: PyPy 1.6 - 1.9

* 1.7x speed improvement overall, lower memory footsprint

* more importantly: we are now reasonably fast on most programs

* packaging: Debian, Ubuntu, Fedora, Homebrew, Gentoo, ArchLinux, ...
  (thanks to all the packagers)

* We joined the SFC (Bradley successfully fighting U.S. bureaucracy) and
  are happy about it

* funding: new model, more than 100'000$ in donations,
  both from a large number of individuals and a few large companies
  and the Python Software Foundation

* Windows (but still no 64-bit)

* Jit hooks, JitViewer

* cpyext moved from 'alpha' to 'beta': it runs e.g. a big part of PyOpenSSL and lxml


Current problems
----------------

* still slow warmup time

* calling C is still an issue


Future
------

* JIT backends: ARMv7, PPC64

* numpy

* cffi (google "CFFI 0.1")

* stackless?  Unclear status, but work might get finished

* stm

