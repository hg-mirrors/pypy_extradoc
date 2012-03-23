Performance analysis tools for JITted VMs
=========================================

When writing code in C, the mapping between written code and compiled assembler
is generally pretty well understood. Compilers employ tricks, but barring
few extreme examples they're, typically within 20% performance difference
from "naive" compilation. Tools used to assess performance are usually
per-function profilers, like valgrind, oprofile or gnuprof. They all can
display time spent per function as well as cumulative times and call
chains. This works very well for small-to-medium programs, however large,
already profiled programs tend to have flat performance profile with unclear
message from profilers.

To make matters even more complicated, in JITted VMs, like PyPy, mapping
between assembler and high level language, like python, is very unclear and
not well known. Writing "good" vs "bad" python (from the JIT perspective),
can make a 20x performance difference.

This talk will cover current profilers available for Python and PyPy,
as well as other tools that can be used to assess performance. I'll also
present in which cases using current tools does not give necessary information
and what kind of tools can address this problem in the future.
