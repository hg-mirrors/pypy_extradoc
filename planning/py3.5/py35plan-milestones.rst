

Milestone 1
-----------

async/await support, and some other general Python 3.4/3.5 features.

For the whole duration of the project we will certainly work on the very
large set of small-scale new features.  These features are listed in
a lot of details in these pages:

* https://docs.python.org/3/whatsnew/3.4.html

* https://docs.python.org/3/whatsnew/3.5.html

Milestone 1 contains only a subset of these features.  We have reached
milestone 1 when we have done all the following point, possibly minus
one of them if it is found during development that properly
implementing it requires significantly more efforts than planned:

* PEP 492, coroutines with async and await syntax.  (The complete PEP
  is included.)

* PEP 465, a new matrix multiplication operator: a @ b.

* PEP 448, additional unpacking generalizations.

* bytes % args, bytearray % args: PEP 461

* New bytes.hex(), bytearray.hex() and memoryview.hex() methods.

* memoryview now supports tuple indexing

* Generators have a new gi_yieldfrom attribute

* A new RecursionError exception is now raised when maximum recursion
  depth is reached.

* The new os.scandir() function

* Newly created file descriptors are non-inheritable (PEP 446)

* The marshal format has been made more compact and efficient

* enum: Support for enumeration types (PEP 435).

* pathlib: Object-oriented filesystem paths (PEP 428).

This includes checking and integrating the code produced by the Summer
of Code student that starts working on some of these features, namely
the first three points above.



Milestone 2
-----------

Changes to the C API.

We get an up-to-date ``cpyext`` module that supports CPython 3.5 C
extension modules, including "argument clinic" and other parts of
the C API that are new.  The goal is that ``cpyext`` works as well
as it does on PyPy2.

Additionaly we resolve several security related issues found in CPython 3.4/3.5:

* Secure and interchangeable hash algorithm (PEP 456).

* New command line option for isolated mode.

* Enhancements to multiprocessing modules.

* HTTP cookie parsing is now stricter (issue 22796).

The measure of when this milestone is reached is based on the
following criteria: we can take a number of C extension modules that
work on CPython 3.5 (without reaching into the internals, like a few
modules do), and check that they work on PyPy 3.5 as well.  More
specifically, for any C module with a 2.7 version that works on PyPy
2.7, its 3.5 equivalent version must also work on PyPy 3.5.


Milestone 3
-----------

ssl and more sustainable stdlib modules with cffi.  Compact unicode
representation.

We get an SSL module compatible with Python 3.5 (more specifically the
latest 3.5.x micro release).  The details of what's new in CPython 3.5
about the SSL module are documented in the two pages linked above.

We also make sure that CFFI works on PyPy 3.5.  At this point either
our SSL module is an extension of the SSL module that exists in PyPy2,
or it was rewritten using CFFI, if we decided that this is the way to
go.

In this milestone is also present the other topic whose details are
still open: to make unicode strings more compact, we may use either
CPython's approach (https://docs.python.org/3/whatsnew/3.3.html#pep-393)
or UTF-8 strings.

Furthermore we will update and resolve more security related issues.
In addition to the ssl related changes we solve the following:

* A new hashlib.pbkdf2_hmac() function.

* TLSv1.1 and TLSv1.2 support for ssl.

* Server-side SNI (Server Name Indication) support for ssl.

* Server certificate verification, including hostname matching and CRLs.

* SSLv3 is now disabled throughout the standard library (issue 22638).

Milestone 4
===========

Benchmarking and performance improvements.

The majority of work in Milestone 4 will be focused on delivering the performance
improvements, which also requires porting PyPy benchmark suite to Python 3. The vast
majority of large library-based benchmarks that are in the PyPy benchmark suite run on
Python 3 these days, so porting of the benchmarks should not be a major problem.

There are a few optimizations that were either disabled in PyPy3 or never ported,
together with some stuff that requires new thinking w.r.t unicode used a bit more
internally in the interpreter source. After porting the benchmark
suite we expect to find them and fix them.

The concrete deliverable will be a release of compliant and performant
PyPy3.5 version together with a blog post describing what we have
done.
