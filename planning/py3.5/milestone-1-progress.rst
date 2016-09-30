What would be cool to finish before the end of Milestone 1
==========================================================


In-progress ("Lock" section)
----------------------------

* richard: bz2, lzma, ... changes (cpython issue 15955) (DONE)
* richard: threads do not seem to join (e.g. lib-python/3/test/test_bz2.py)

* arigo: faulthandler module



Misc stuff not formally in any milestone
----------------------------------------

* At some point, review lib-python/conftest.py to remove the skips
  due to deadlocks (search for "XXX:")

* collections.py: ``OrderedDict`` should again be a thin wrapper over
  ``dict``.  The main pain point is ``move_to_end(last=False)``.  See
  https://mail.python.org/pipermail/python-dev/2016-August/145837.html

* compare ``dir(posix)`` on py3.5 and cpython 3.5.

* ``KeyError('pip.exceptions',) in weakref callback <function
  _get_module_lock.<locals>.cb at 0x00007f118e2c0020> ignored``
  we're getting them now on start-up, investigate

* ``print 5`` should give
  ``SyntaxError: Missing parentheses in call to 'print'``

* Windows: issue 2310: kill WindowsError

* bytearray: 'del x[:10]' is now amortized constant-time

* check that 'import array', say, finds and loads a file array.py,
  whereas 'import gc' does not ('gc' is a built-in module in CPython but
  'array' is typically an extension module; at least that's the case on
  Linux with default compilation settings).

* 'import stackless' fails


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

* bytes % args, bytearray % args: PEP 461

* New bytes.hex(), bytearray.hex() and memoryview.hex() methods. (DONE)

* memoryview now supports tuple indexing (DONE)

* A new RecursionError exception is now raised when maximum recursion
  depth is reached. (DONE)

* The new os.scandir() function (POSIX-DONE, missing Win32)

* Newly created file descriptors are non-inheritable (PEP 446) 
  (POSIX-DONE, missing Win32)

* The marshal format has been made more compact and efficient
  (DONE, maybe a small optimization left---TYPE_*ASCII*---that
  depends on compact unicode representation)

* enum: Support for enumeration types (PEP 435). (PURELY-APPLEVEL)

* pathlib: Object-oriented filesystem paths (PEP 428). (PURELY-APPLEVEL)
