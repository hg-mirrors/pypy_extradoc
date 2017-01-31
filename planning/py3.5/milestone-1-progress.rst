What would be cool to finish before the end of Milestone 1
==========================================================


In-progress ("Lock" section)
----------------------------


Misc stuff not formally in any milestone
----------------------------------------

moved to milestone-2-progress.rst


Milestone 1 (Aug-Sep-Oct 2016)
------------------------------

We have reached milestone 1 when we have done all the following point,
possibly minus one of them if it is found during development that
properly implementing it requires significantly more efforts than
planned:

* PEP 492, coroutines with async and await syntax.  (The complete PEP
  is included.)  DONE

* PEP 465, a new matrix multiplication operator: a @ b.

* PEP 448, additional unpacking generalizations.

* bytes % args, bytearray % args: PEP 461 (DONE)

* New bytes.hex(), bytearray.hex() and memoryview.hex() methods. (DONE)

* memoryview now supports tuple indexing (DONE)

* A new RecursionError exception is now raised when maximum recursion
  depth is reached. (DONE)

* The new os.scandir() function (POSIX-DONE, missing Win32)

* Newly created file descriptors are non-inheritable (PEP 446) 
  (DONE)

* The marshal format has been made more compact and efficient
  (DONE, maybe a small optimization left---TYPE_*ASCII*---that
  depends on compact unicode representation)

* enum: Support for enumeration types (PEP 435).
  the is a pypi package called enum34 that implements it (pure python maybe?)

* pathlib: Object-oriented filesystem paths (PEP 428). (PURELY-APPLEVEL)

Done not formally in the Milestone
----------------------------------

* richard: bz2, lzma, ... changes (cpython issue 15955) (DONE)
* richard: threads do not seem to join (e.g. lib-python/3/test/test_bz2.py) (DONE)
* richard: cffi ssl (DONE, awaits review + merge)
