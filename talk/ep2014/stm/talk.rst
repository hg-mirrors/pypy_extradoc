------------------------------------------------------------------------------
Using All These Cores: Transactional Memory in PyPy
------------------------------------------------------------------------------

.. raw:: html

    <center>

**Armin Rigo - EuroPython 2014**

.. raw:: html

    </center>


Part 1 - Intro and Current Status
---------------------------------


Introduction
------------

* PyPy-STM: Software Transactional Memory

* On-going research project:

  - by Remi Meier and myself
  - helped by crowdfunding, thanks to all donors

* Started as a EuroPython 2011 lightning talk


Why is there a GIL?
-------------------

* GIL = Global Interpreter Lock

* initially: CPython was single threaded

* for concurrency (but not parallelism):

  - provide concurrently running threads

* easiest way to retrofit into interpreter:

  - acquire GIL around the execution of bytecode instructions

  - easy for refcounting, too


Consequences (+)
----------------

* atomic & isolated instructions:

  - things like ``list.append()`` are atomic
  - tons of websites mention this
  - latent races if Python becomes really parallel

* sequential consistency:

  - less surprises; "all variables volatile"


Consequences (-)
----------------

* obviously, no parallelism

* GIL not available to application:
    
  - all difficulties of concurrency still there
  - need application-level locking


Removing the GIL
----------------

* 1. Fine-grained locking

* 2. Shared-nothing

* 3. Transactional memory


Fine-grained locking
--------------------

* replace GIL with locks on objs / data structures

* accessing different objects can run in parallel

* harder to implement:

  - many locks -> deadlock risks
  - refcounting issue

* overhead of lock/unlock on objs:

  - Jython depends on JVM for good lock removal

* still need application-level locking


Shared-nothing
--------------

* each independent part of the program gets its own interpreter

* simple implementation

* gives workaround instead of direct replacement

* not compatible to existing threaded applications, a priori

* explicit communication:

  - good: clean model, no locks
  - bad: limitations, overhead


Transactional Memory
--------------------

* like GIL, but instead of blocking, each thread runs optimistically

* "easy" to implement:

  - GIL acquire -> transaction start

  - GIL release -> transaction commit

* overhead: cross-checking conflicting memory reads and writes,
  and if necessary, cancel and restart transactions

* HTM, STM, or some hybrids exist:
    
  - but mostly still research-only


PyPy-STM
--------

* implementation of a specially-tailored STM ("hard" part):
    
  - a reusable C library
  - called STMGC-C7

* used in PyPy to replace the GIL ("easy" part)

* could also be used in CPython

  - but refcounting needs replacing


How does it work?
-----------------

.. image:: fig4.svg


Demo
------

* counting primes


Long Transactions
----------------------------

* threads and application-level locks still needed...

* but *can be very coarse:*

  - two transactions can optimistically run in parallel

  - even if they both *acquire and release the same lock*


Long Transactions
-----------------

.. image:: fig4.svg


Demo
------

* Bottle web server


PyPy-STM Programming Model
---------------------------

* threads-and-locks, fully compatible with the GIL

* this is not "everybody should use careful explicit threading
  with all the locking issues"

* instead, PyPy-STM pushes forward:

  - make or use a thread pool library

  - coarse locking, inside that library only


PyPy-STM Programming Model
--------------------------

* e.g.:

  - ``multiprocessing``-like thread pool

  - Twisted/Tornado/Bottle extension

  - Stackless/greenlet/gevent extension


PyPy-STM status
---------------

* current status:

  - basics work
  - best case 25-40% overhead (much better than originally planned)
  - app locks not done yet ("with atomic" workaround)
  - tons of things to improve
  - tons of things to improve
  - tons of things to improve
  - tons of things to improve
  - tons of things to improve
  - tons of things to improve
  - tons of things to improve


Summary: Benefits
-----------------

* Potential to enable parallelism:

  - in any CPU-bound multithreaded program

  - or as a replacement of ``multiprocessing``

  - but also in existing applications not written for that

  - as long as they do multiple things that are "often independent"

* Keep locks coarse-grained


Summary: Issues
---------------

* Keep locks coarse-grained:

  - but in case of systematic conflicts, performance is bad again

  - need to track and fix them

  - need tool to support this (debugger/profiler)

* Performance hit: 25-40% slower than a plain PyPy-JIT (may be ok)


Summary: PyPy-STM
-----------------

* Not production-ready

* But it has the potential to enable "easier parallelism for everybody"

* Still alpha but slowly getting there!

  - see http://morepypy.blogspot.com/

* Crowdfunding!

  - see http://pypy.org/


Part 2 - Under The Hood
-----------------------

**STMGC-C7**


Overview
--------

* Say we want to run N = 2 threads

* We reserve twice the memory

* Thread 1 reads/writes "memory segment" 1

* Thread 2 reads/writes "memory segment" 2

* Upon commit, we (try to) copy the changes to the other segment


Trick #1
--------

* Objects contain pointers to each other

* These pointers are relative instead of absolute:

  - accessed as if they were "thread-local data"

  - the x86 has a zero-cost way to do that (``%fs``, ``%gs``)

  - supported in clang (not gcc so far)


Trick #2
--------

* With Trick #1, most objects are exactly identical in all N segments:

  - so we share the memory
  
  - ``mmap() MAP_SHARED``

  - actual memory usage is multiplied by much less than N

* Newly allocated objects are directly in shared pages:
    
  - we don't actually need to copy *all new objects* at commit,
    but only the few *old objects* modified


Barriers
--------

* Need to record all reads and writes done by a transaction

* Extremely cheap way to do that:

  - *Read:* set a flag in thread-local memory (one byte)

  - *Write* into a newly allocated object: nothing to do

  - *Write* into an old object: add the object to a list

* Commit: check if each object from that list conflicts with
  a read flag set in some other thread


...
-------------------


Thank You
---------

* http://morepypy.blogspot.com/

* http://pypy.org/

* irc: ``#pypy`` on freenode.net
