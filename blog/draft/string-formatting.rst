PyPy is faster than C, again: string formatting
===============================================

String formatting is probably something you do just about every day in Python,
and never think about.  It's so easy, just ``"%d %d" % (i, i)`` and you're
done.  No thinking about how to size your result buffer, whether your output
has an appropriae NULL byte at the end, or any other details.  A C
equivilant might be::

    char x[41];
    sprintf(x, "%d %d", i, i);

Note that we had to stop for a second and consider how big numbers might get
and overestimate the size (41 = length of the biggest number on 64bit + 1 for
the sign).
This is fine, except you can't even return ``x`` from this function, a more
fair comparison might be::

    char *x = malloc(41 * sizeof(char));
    sprintf(x, "%d %d", i, i);

``x`` is slightly overallocated in some situations, but that's fine.

But we're not here to discuss the exact syntax of string formatting, we're here
to discuss how blazing fast PyPy is at it, with the new ``unroll-if-alt``
branch.  Given the Python code::

    def main():
        for i in xrange(10000000):
            "%d %d" % (i, i)

    main()

and the C code::

    #include <stdio.h>
    #include <stdlib.h>


    int main() {
        int i = 0;
        char x[41];
        for (i = 0; i < 10000000; i++) {
            sprintf(x, "%d %d", i, i);
        }
    }

Ran under PyPy, at the head of the ``unroll-if-alt`` branch, and compiled with
GCC 4.5.2 at -O4 (other optimization levels were tested, this produced the best
performance). It took .85 seconds to execute under PyPy, and 1.63 seconds with
the compiled binary. We think this demonstrates the incredible potential of
dynamic compilation, GCC is unable to inline or unroll the ``sprintf`` call,
because it sits inside of libc.

Benchmarking the C code::

    #include <stdio.h>
    #include <stdlib.h>


    int main() {
        int i = 0;
        for (i = 0; i < 10000000; i++) {
            char *x = malloc(23 * sizeof(char));
            sprintf(x, "%d %d", i, i);
            free(x);
        }
    }

Which as discussed above, is more comperable to the Python, takes 1.93 seconds.
