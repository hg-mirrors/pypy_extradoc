
=====================================
Software Transactional Memory on PyPy
=====================================


Pseudo-Goal
-----------

* "Kill the GIL"

* GIL = Global Interpreter Lock


Real Goals
----------

* Multi-core programming

* But *reasonable* multi-core programming

* Using the recent model of Transactional Memory


PyPy-STM
--------

* An executable ``pypy-stm`` which uses internally
  Software Transactional Memory

* Optimistically run multiple threads in parallel

* The only new feature is ``atomic``:

.. sourcecode:: python

    with atomic:
        piece of code...


Example of higher-level API
---------------------------

.. sourcecode:: python

    def work(...):
        ...
        several more calls to: 
            transaction.add(work, ...)
        ...


* Starts N threads, scheduling `work()` calls to them

* Each `work()` is done in an ``atomic`` block

* Multi-core, but as if all the `work()` are done sequentially


Q&A
---

* Thank you!

* Budget of $10k left, likely more needed too
