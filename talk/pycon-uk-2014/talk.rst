.. include:: beamerdefs.txt

===========================
PyPy and its ecosystem
===========================

About me
---------

- PyPy core dev

- Working on HippyVM


What is PyPy?
--------------

- "PyPy is a fast, compliant alternative implementation of the Python language (2.7.8 and 3.2.5)."

- Python interpreter

  * written in RPython

  * **FAST**


What is RPython?
----------------

- Subset of Python

  * easy to read

  * easy to test

- JIT & GC for free

- General framework for dynamic languages


RPython-powered languages
-------------------------

- **PyPy**

- HippyVM: implementing PHP

  * ~7x faster than standard PHP

  * http://hippyvm.com/

- Topaz: implementing Ruby

  * most of the language implemented

  * "definitely faster than MRI"

  * https://github.com/topazproject/topaz

- Pyrolog (Prolog)

- RTruffleSOM (Smalltalk)

- RSqueakVM (Smalltalk)

- lang-js (JavaScript)


RPython translation stages
--------------------------

- (R)Python code

|pause|

- ``import``

  * Python objects (functions, classes, ...)

|pause|

- Bytecode analysis, type inference

  * Typed control flow graph

|pause|

- Translator transformations

  * Add GC & JIT

|pause|

- Code generation

  * C code

|pause|

- ``gcc``

  * Compiled executable


How does the JIT work?
----------------------

|pause|

- "Jitcode": very low-level byte code

  * Translates to machine code

- Translation time

  * Add jitcode representation to RPython functions

- Run-time:

  * Detect **hot** loop

  * Trace one code path through the loop

  * Compile (magic!)

  * Profit!


RPython example (HippyVM)
-------------------------

|scriptsize|

.. code:: python

    @wrap(['space', str, W_Root, Optional(int)])
    def strpos(space, haystack, w_needle, offset=0):
        """Find the position of the first occurrence of a substring in a string."""
        if offset < 0 or offset > len(haystack):
            space.ec.warn("strpos(): Offset not contained in string")
            return space.w_False
        try:
            needle = unwrap_needle(space, w_needle)
        except ValidationError as exc:
            space.ec.warn("strpos(): " + exc.msg)
            return space.w_False
        if len(needle) == 0:
            space.ec.warn("strpos(): Empty needle")
            return space.w_False

        result = haystack.find(needle, offset)

        if result == -1:
            return space.w_False
        return space.newint(result)

|end_scriptsize|

PyPy: past two years (1)
-----------------------------

- PyPy 2.0 (May 2013)

  * Beta ARM, CFFI, unicode performance

  * stackless + JIT (eventlet, gevent, ...)

|pause|

- PyPy 2.1 (July 2013)

  * Stable ARM

  * py3k (3.2.3), numpy, general improvements, bugfixes

|pause|

- PyPy 2.2 (November 2013)

  * Incremental GC, faster JSON

  * More JIT, more py3k

  * More numpy, numpy C API


PyPy: past two years (2)
-------------------------

- PyPy 2.3 (May 2014)

  * Lot of internal refactoring

  * C API for embedding

  * General improvements

|pause|

- PyPy 2.4 (coming soon!)

  * Python 2.7.8 stdlib

  * General fixes and improvements 


Current status
---------------

- Python code: "it just works"

- C code: better than ever!

  * cpyext: more complete, but still slow

  * CFFI: the future

  * Native PyPy C API for embedding

  * cppyy for C++

- Lots of CFFI modules around:

  * pygame_cffi, psycopg2_cffi, lxml

- numpy: in-progress (more later)


Speed: 6.3x faster than CPython
--------------------------------

.. image:: speed.png
   :scale: 47%


ARM
----

- Official support since PyPy 2.1

- "it just works"

- ~7.5x faster than CPython on ARM

- Thanks to Raspberry-Pi foundation

- Distributed as part of Raspbian OS


py3k
----

- 3.2: stable

- 3.3: branch started, in-progress

- Some missing optimizations

  * getting better


CFFI
-----

- Python <-> C interfacing done right

  * existing shared libraries

  * custom C code

- Inspired by LuaJIT's FFI

- Alternative to C-API, ctypes, Cython, etc.

- Fast on CPython, super-fast on PyPy


numpy
-----

- As usual, in-progress

- ~80% of numpy implemented

  * 2336 passing tests out of 3265

  * http://buildbot.pypy.org/numpy-status/latest.html

- Just try it

- No scipy :-/


cppyy
------

- Interface to C++

- Based on reflection, no need to write wrappers

- PyPy-only, similar to PyCintex for CPython

- Main use case: ROOT

  * http://root.cern.ch

  * "a set of OO frameworks with all the functionality needed to handle and
    analyze large amounts of data in a very efficient way"

- 3x faster than CPython


The future: STM
----------------

- Software Transactional Memory

- Strategy to solve race conditions

- "Finger crossed", rollback in case of conflicts

- On-going research project

  * by Armin Rigo and Remi Meier

STM semantics
-------------

- N threads

- Each thread split into atomic blocks

- Sequential execution in some arbitrary order

- In practice:

- Parallel execution, conflicts solved by STM


Unit of execution (1)
---------------------

- Atomic blocks == 1 Python bytecode

- Threads are executed in arbitrary order, but bytecodes are atomic

- ==> Same semantics as GIL

- "and this will solve the GIL problem" (A. Rigo, EuroPython 2011 lighting talk)

Unit of execution (2)
----------------------

- Larger atomic blocks

- ``with atomic:``

- Much easier to use than explicit locks

- Can be hidden by libraries to provide even higher level paradigms

  * e.g.: Twisted apps made parallel out of the box

Race conditions
---------------

- They don't magically disappear

- With explicit locks

  * ==> BOOM

  * you fix bugs by preventing race conditions

- With atomic blocks

  * ==> Rollback

  * Performance penalty

  * You optimize by preventing race conditions

- Fast&broken vs. Slower&correct


Implementation
---------------

- Conflicts detection, commit and rollback is costly

- Original goal (2011): 2x-5x slower than PyPy without STM

  * But parallelizable!

|pause|

- Current goal (2014): 25% slower than PyPy without STM

- Yes, that's 10x less overhead than original goal

- mmap black magic

Current status
---------------

- Preliminary versions of pypy-jit-stm available

- The JIT overhead is still a bit too high

- Lots of polishing needed


Fundraising campaign
---------------------

- py3k: 52,380 $ of 105,000 $ (49.9%)

- numpy: 48,412 $ of 60,000 $ (80.7%)

- STM, 1st call: 25,000 $

- STM, 2nd call: 13,939 $ of 80,000 $ (17.4%)

- Thanks to all donors!


Contacts, Q&A
--------------

- http://pypy.org

- http://morepypy.blogspot.com/

- IRC: #pypy@freenode.net

- Any question?
