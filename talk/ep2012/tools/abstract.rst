Performance analysis tools for JITted VMs
=========================================

When writing code in C, the mapping between written code and compiled assembler
is generally pretty well understood. Compilers employ tricks, but barring
few extreme examples they're, typically within 20% performance difference
from "naive" compilation. Tools used to asses performance are usually
per-function profilers, like valgrind, oprofile or gnuprof. They all can
display time spent per function as well as cumultative times and call
chains. This works very well for small-to-medium programs, however large,
already profiled programs tend to have flat performance profile with unclear
message from profilers.

To make matters even more complicated, in JITted VMs, like PyPy, mapping
between assembler and high level language, like python, is very unclear and
not well known. Writing "good" vs "bad" python (from the JIT perspective),
can make a 20x performance difference. I would like to show current profilers,
their use cases and shortcomings as well as make the case that we need much
better tools to deal with the current situation.
