Abstract
--------

As part of the PyPy project, we explore the usage of transactional
memory (TM) to enable parallelism for high-level, dynamic languages like
Python or Ruby.

Most current software TM (STM) systems suffer from a big overhead when
they run on a single thread only (usually between 2-5x slowdown). They
try to scale to a large number of CPUs for the benefit of
parallelization to be greater than the penalty of the overhead. On the
other hand, while also software-based, the system presented here
initially focuses on a low CPU count (< 8). It uses an approach that can
keep the single-thread overhead very low (initial experiments with a
simple lisp interpreter suggest around 15%). As a consequence we already
see great speed-ups over single-threaded, non-STM execution by only
using 2 CPU cores. We achieve this with very-low-overhead read barriers
and very-low-overhead fast paths of write barriers. The enabling
mechanism, the Linux-only system call "remap_file_pages", allows for
creating several "views" on partially shared memory; every thread sees
one of these views.

Our goal is to support a mixture of short to very long transactions.  We
have an object-based STM system with an integrated GC handling the
typical high allocation rates of dynamic languages; in particular, it is
a generational GC, and the write barrier combines GC and STM roles,
always taking the fast path for recently-allocated objects.

The next step is to finish integrating this system with PyPy, the Python
interpreter in Python, and its Just-In-Time compiler.  This is
relatively straightforward and partly done already.  We believe that the
result has got the potential to give good enough performance to rival or
exceed the HTM experiments which have been done before on Ruby [1].
Future considerations also include optionally adding a hybrid (HyTM)
component to our system.


--------

[1] Eliminating Global Interpreter Locks in Ruby through Hardware
Transactional Memory.

Rei Odaira, Jose G. Castanos and Hisanobu Tomari.

PPoPP '14 Proceedings of the 19th ACM SIGPLAN symposium on Principles and practice of parallel programming

Pages 131-142
