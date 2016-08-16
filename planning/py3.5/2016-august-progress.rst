August 2016
===========

Planned
-------

* Implement changes to memory view. e.g. hex(): https://bugs.python.org/issue9951 (plan_rich)

* Make a translated py3.5 actually work a bit (currently we get
  systematic failures), up to the point where we can meaningfully
  run the lib-python tests (arigo)

Finished
--------



Milestone 1 (Aug-Sep-Oct 2016)
------------------------------

We have reached milestone 1 when we have done all the following point,
possibly minus one of them if it is found during development that
properly implementing it requires significantly more efforts than
planned:

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
