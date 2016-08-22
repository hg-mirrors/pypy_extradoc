August 2016
===========

Planned
-------

* Implement changes to memory view. e.g. hex(): https://bugs.python.org/issue9951 (plan_rich)
  Seems to work, but test suite hangs to verify the CPython tests.
* tuple indexing for memory view (plan_rich)
  Comments: Stronly tied to numpy. Hard to implement, because most of the basics are missing (dimensions/strides)
  We should make a plan to impl. that on default with cpyext support and merge it back to py3.5.
  Matti's opinion on that would be great!


Finished
--------


Not in any milestone
--------------------

* At some point, review lib-python/conftest.py to remove the skips
  due to deadlocks (search for "XXX:")

* collections.py: ``OrderedDict`` should again be a thin wrapper over
  ``dict``.  The main pain point is ``move_to_end(last=False)``.  See
  https://mail.python.org/pipermail/python-dev/2016-August/145837.html


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
  depth is reached. (DONE)

* The new os.scandir() function (POSIX-DONE, missing Win32)

* Newly created file descriptors are non-inheritable (PEP 446)

  - added rposix.{set,get}_inheritable(), used it as a quick hack
    inside interp_posix.pipe(), needed otherwise subprocess.Popen()
    deadlocks

* The marshal format has been made more compact and efficient

* enum: Support for enumeration types (PEP 435).

* pathlib: Object-oriented filesystem paths (PEP 428).
