======================
PyPy 2.0 alpha for ARM
======================

Hello.

We're pleased to announce an alpha release of PyPy 2.0 for ARM. This is mostly
a technology preview, as we know the JIT is not yet stable enough for the
full release. However please try your stuff on ARM and report back.

This is the first release that supports a range of ARM devices - anything with
ARMv6 (like the Raspberry Pi) or ARMv7 (like Beagleboard, Chromebook,
Cubieboard, etc.) that supports VFPv3 should work. We provide builds with
support for both ARM EABI variants, hard-float and for some older operating
systems soft-float.

This release comes with a list of limitations, consider it alpha quality,
not suitable for production:

* stackless support is missing.

* assembler produced is not always correct, but we successfully managed to
  run large parts of our extensive benchmark suite, so most stuff should work.

You can download the PyPy 2.0 alpha ARM release here:

    http://pypy.org/download.html 

Part of the work was sponsored by the `Raspberry Pi foundation`_.

.. _`Raspberry Pi foundation`: http://www.raspberrypi.org/

What is PyPy?
=============

PyPy is a very compliant Python interpreter, almost a drop-in replacement for
CPython 2.7.3. It's fast due to its integrated tracing JIT compiler.

This release supports ARM machines running Linux 32bit. Both hard-float
``armhf`` and soft-float ``armel`` builds are provided.  ``armhf`` builds are
created using the Raspberry Pi custom `cross-compilation toolchain`_ based on
gcc-arm-linux-gnueabihf and should work on ARMv6 and ARMv7 devices running at
least debian or ubuntu. ``armel`` builds are built using gcc-arm-linux-gnuebi
toolchain provided by ubuntu and currently target ARMv7.  If there is interest
in other builds, such as gnueabi for ARMv6 or without requiring a VFP let us
know in the comments or in IRC.

.. _`cross-compilation toolchain`: https://github.com/raspberrypi

Benchmarks
==========

Everybody loves benchmarks. Here is a table of our benchmark suite
(for ARM we don't provide it yet on http://speed.pypy.org,
unfortunately).

This is a comparison of Cortex A9 processor with 4M cache and Xeon W3580 with
8M of L3 cache. The set of benchmarks is a subset of what we run for
http://speed.pypy.org that finishes in reasonable time. The ARM machine
was provided by Calxeda.
Columns are respectively:

* benchmark name

* PyPy speedup over CPython on ARM

* PyPy speedup over CPython on x86

* speedup on Xeon vs Cortex A9, as measured on CPython

* speedup on Xeon vs Cortex A9, as measured on PyPy

* relative speedup (how much bigger the x86 speedup is over ARM speedup)

+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| Benchmark          | PyPy vs CPython (arm) | PyPy vs CPython (x86) | x86 vs arm (pypy) | x86 vs arm (cpython) | relative speedup |
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| ai                 | 3.61                  | 3.16                  | 7.70              | 8.82                 | 0.87             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| bm_mako            | 3.41                  | 2.11                  | 8.56              | 13.82                | 0.62             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| chaos              | 21.82                 | 17.80                 | 6.93              | 8.50                 | 0.82             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| crypto_pyaes       | 22.53                 | 19.48                 | 6.53              | 7.56                 | 0.86             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| django             | 13.43                 | 11.16                 | 7.90              | 9.51                 | 0.83             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| eparse             | 1.43                  | 1.17                  | 6.61              | 8.12                 | 0.81             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| fannkuch           | 6.22                  | 5.36                  | 6.18              | 7.16                 | 0.86             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| float              | 5.22                  | 6.00                  | 9.68              | 8.43                 | 1.15             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| go                 | 4.72                  | 3.34                  | 5.91              | 8.37                 | 0.71             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| hexiom2            | 8.70                  | 7.00                  | 7.69              | 9.56                 | 0.80             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| html5lib           | 2.35                  | 2.13                  | 6.59              | 7.26                 | 0.91             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| json_bench         | 1.12                  | 0.93                  | 7.19              | 8.68                 | 0.83             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| meteor-contest     | 2.13                  | 1.68                  | 5.95              | 7.54                 | 0.79             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| nbody_modified     | 8.19                  | 7.78                  | 6.08              | 6.40                 | 0.95             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| pidigits           | 1.27                  | 0.95                  | 14.67             | 19.66                | 0.75             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| pyflate-fast       | 3.30                  | 3.57                  | 10.64             | 9.84                 | 1.08             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| raytrace-simple    | 46.41                 | 29.00                 | 5.14              | 8.23                 | 0.62             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| richards           | 31.48                 | 28.51                 | 6.95              | 7.68                 | 0.91             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| slowspitfire       | 1.28                  | 1.14                  | 5.91              | 6.61                 | 0.89             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| spambayes          | 1.93                  | 1.27                  | 4.15              | 6.30                 | 0.66             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| sphinx             | 1.01                  | 1.05                  | 7.76              | 7.45                 | 1.04             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| spitfire           | 1.55                  | 1.58                  | 5.62              | 5.49                 | 1.02             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| spitfire_cstringio | 9.61                  | 5.74                  | 5.43              | 9.09                 | 0.60             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| sympy_expand       | 1.42                  | 0.97                  | 3.86              | 5.66                 | 0.68             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| sympy_integrate    | 1.60                  | 0.95                  | 4.24              | 7.12                 | 0.60             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| sympy_str          | 0.72                  | 0.48                  | 3.68              | 5.56                 | 0.66             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| sympy_sum          | 1.99                  | 1.19                  | 3.83              | 6.38                 | 0.60             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| telco              | 14.28                 | 9.36                  | 3.94              | 6.02                 | 0.66             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| twisted_iteration  | 11.60                 | 7.33                  | 6.04              | 9.55                 | 0.63             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| twisted_names      | 3.68                  | 2.83                  | 5.01              | 6.50                 | 0.77             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+
| twisted_pb         | 4.94                  | 3.02                  | 5.10              | 8.34                 | 0.61             | 
+--------------------+-----------------------+-----------------------+-------------------+----------------------+------------------+

It seems that Cortex A9, while significantly slower than Xeon, has higher
slowdowns with a large interpreter (CPython) than a JIT compiler (PyPy). This
comes as a surprise to me, especially that our ARM assembler is not nearly
as polished as our x86 assembler. As for the causes, various people mentioned
branch predictor, but I would not like to speculate without actually knowing.

How to use PyPy?
================

We suggest using PyPy from a `virtualenv`_. Once you have a virtualenv
installed, you can follow instructions from `pypy documentation`_ on how
to proceed. This document also covers other `installation schemes`_.

.. _`pypy documentation`: http://doc.pypy.org/en/latest/getting-started.html#installing-using-virtualenv
.. _`virtualenv`: http://www.virtualenv.org/en/latest/
.. _`installation schemes`: http://doc.pypy.org/en/latest/getting-started.html#installing-pypy
.. _`PyPy and pip`: http://doc.pypy.org/en/latest/getting-started.html#installing-pypy

We would not recommend using PyPy on ARM just quite yet, however the day
of a stable PyPy ARM release is not far off.

Cheers,
fijal, bivab, arigo and the whole PyPy team
