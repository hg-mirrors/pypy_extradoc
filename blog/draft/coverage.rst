Making coverage.py faster under PyPy
====================================

If you've ever tried to run your programs with ``coverage.py`` under PyPy,
you've probably experienced some incredible slowness. Take this simple
program:

.. source-code:: python

    def f():
        return 1


    def main():
        i = 10000000
        while i:
            i -= f()

    main()

Running ``time coverage.py run test.py`` five times, and looking at the best
run, here's how PyPy 2.1 stacks up against CPython 2.7.5:

+---------------+---------+-----------------------+
| Python        | Time    | Normalized to CPython |
+===============+=========+=======================+
| CPython 2.7.5 | 3.879s  | 1.0x                  |
+---------------+---------+-----------------------+
| PyPy 2.1      | 53.330s | 13.7x slower          |
+---------------+---------+-----------------------+

Totally ridiculous. I got turned onto this problem because on one of my
projects CPython takes about 1.5 minutes to run our test suite on the build
bot, but PyPy takes 8-10 minutes.

So I sat down to address it. And the results:

+---------------+---------+-----------------------+
| Python        | Time    | Normalized to CPython |
+===============+=========+=======================+
| CPython 2.7.5 | 3.879s  | 1.0x                  |
+---------------+---------+-----------------------+
| PyPy 2.1      | 53.330s | 13.7x slower          |
+---------------+---------+-----------------------+
| PyPy head     | 1.433s  | 2.7x faster           |
+---------------+---------+-----------------------+

Not bad.

Technical details
-----------------

So how'd we do it? Previously, using ``sys.settrace()`` (which ``coverage.py``
uses under the hood) disabled the JIT. Except it didn't just disable the JIT,
it did it in a particularly insidious way — the JIT had no idea it was being
disabled!

Instead, every time PyPy discovered that one of your functions was a hotspot,
it would start tracing to observe what the program was doing, and right when it
was about to finish, ``coverage`` would run and cause the JIT to abort. Tracing
is a slow process, it makes up for it by generating fast machine code at the
end, but tracing is still incredibly slow. But we never actually got to the
"generate fast machine code" stage. Instead we'd pay all the cost of tracing,
but then we'd abort, and reap none of the benefits.

To fix this, we adjusted some of the heuristics in the JIT, to better show it
how ``sys.settrace(<tracefunc>)`` works. Previously the JIT saw it as an opaque
function which gets the frame object, and couldn't tell whether or not it
messed with the frame object. Now we let the JIT look inside the
``<tracefunc>`` function, so it's able to see that ``coverage.py`` isn't
messing with the frame in any weird ways, it's just reading the line number and
file path out of it.

I asked several friends in the VM implementation and research field if they
were aware of any other research into making VMs stay fast when debugging tools
like ``coverage.py`` are running. No one I spoke to was aware of any (but I
didn't do a particularly exhaustive review of the literature, I just tweeted at
a few people), so I'm pleased to say that PyPy is quite possibly the first VM
to work on optimizing code in debugging mode! This is possible because of our
years spent investing in meta-tracing research.

Happy testing,
Alex
