PyPy is faster than C, again: string formatting
===============================================

String formatting is probably something you do just about every day in Python,
and never think about.  It's so easy, just ``"%d %d" % (i, i)`` and you're
done.  No thinking about how to size your result buffer, whether your output
has an appropriate NULL byte at the end, or any other details.  A C
equivalent might be::

    char x[44];
    sprintf(x, "%d %d", i, i);

Note that we had to stop for a second and consider how big numbers might get
and overestimate the size (44 = length of the biggest number on 64bit (20) +
1 for the sign * 2 + 1 (for the space) + 1 (NUL byte)): it took the authors of
this post, fijal and alex, 3 tries to get the math right on this :-)

This is fine, except you can't even return ``x`` from this function because
it's allocated on the stack. A more fair comparison might be::

    char *x = malloc(44 * sizeof(char));
    sprintf(x, "%d %d", i, i);

``x`` is slightly overallocated in some situations, but that's fine.

But we're not here to just discuss the implementation of string
formatting, we're here to discuss how blazing fast PyPy is at it, with
the new ``unroll-if-alt`` branch.  Given the Python code::

    def main():
        for i in xrange(10000000):
            "%d %d" % (i, i)

    main()

and the C code::

    #include <stdio.h>
    #include <stdlib.h>


    int main() {
        int i = 0;
        char x[44];
        for (i = 0; i < 10000000; i++) {
            sprintf(x, "%d %d", i, i);
        }
    }

Run under PyPy, at the head of the ``unroll-if-alt`` branch, and
compiled with GCC 4.5.2 at -O4 (other optimization levels were tested,
this produced the best performance). It took **0.85** seconds to
execute under PyPy, and **1.63** seconds with the compiled C binary. We
think this demonstrates the incredible potential of dynamic
compilation, GCC is unable to inline or unroll the ``sprintf`` call,
because it sits inside of libc.

Benchmarking the C code::

    #include <stdio.h>
    #include <stdlib.h>


    int main() {
        int i = 0;
        for (i = 0; i < 10000000; i++) {
            char *x = malloc(44 * sizeof(char));
            sprintf(x, "%d %d", i, i);
            free(x);
        }
    }

Which as discussed above, is more comparable to the Python one, gives a
result of **1.96** seconds.

Summary of performance:

+---------------+--------------+--------------+---------+----------------------+
| Platform      | GCC (stack)  | GCC (malloc) | CPython | PyPy (unroll-if-alt) |
+---------------+--------------+--------------+---------+----------------------+
| Time          |        1.63s |        1.96s |   10.2s |                0.85s |
+---------------+--------------+--------------+---------+----------------------+
| relative to C |           1x |        0.83x |   0.16x |             **1.9x** |
+---------------+--------------+--------------+---------+----------------------+

Overall PyPy is almost **2x** faster. This is clearly win for dynamic
compilation over static - the ``sprintf`` function lives in libc and so
cannot be specializing over the constant string, which has to be parsed
every time it's executed. In the case of PyPy, we specialize
the assembler if we detect the left hand string of the modulo operator
to be constant.

Cheers,
alex & fijal
