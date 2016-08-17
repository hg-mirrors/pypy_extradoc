Speeding up existing code using PyPy
====================================

Brief outline:

I spent quite some time profiling existing python programs under PyPy.
This talk will walk through an existing Python library (undecided which yet)
and showcase how to write benchmarks, how to find bottlenecks, how to analyze
them and how to improve them when running on the PyPy interpreter and what
are the theoretical and pracitcal limits.

Detailed abstract:

In this talk I would like to share my experience when optimizing existing
Python codebases. I spend copious amounts of time staring at profiling data,
improving profilers to see anything and improving PyPy to work better
on real-life workloads. I would like to give the audience insight what
sort of constructs are optimized by PyPy, what sort of constructs can
possibly be optimized and which ones are out of question. This talk is
an intermediate one and assumes good enough knowledge of Python to understand
code of a given library (Twisted, Django, Flask, Gunicorn and some stdlib
module are potential candidates), however no prior knowledge of PyPy or
the processor performance characteristics is necessary.
