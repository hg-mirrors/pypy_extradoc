What would be cool to finish before the end of Milestone 1
==========================================================


In-progress ("Lock" section)
----------------------------

* richard: Implement changes to memory view. e.g. hex(): https://bugs.python.org/issue9951
  Seems to work, but test suite hangs to verify the CPython tests.
* richard: tuple indexing for memory view,
  Comments: Stronly tied to numpy. Hard to implement, because most of the basics are missing (dimensions/strides)
  We should make a plan to impl. that on default with cpyext support and merge it back to py3.5.
  Matti's opinion on that would be great!
* richard: extended slicing for memory view
* richard: bytes % args, bytearray % args: PEP 461

* arigo: look at test failures relaced to os.scandir() or the pathlib
  module, or the enum module



Misc stuff not formally in any milestone
----------------------------------------

* At some point, review lib-python/conftest.py to remove the skips
  due to deadlocks (search for "XXX:")

* collections.py: ``OrderedDict`` should again be a thin wrapper over
  ``dict``.  The main pain point is ``move_to_end(last=False)``.  See
  https://mail.python.org/pipermail/python-dev/2016-August/145837.html

* interpreter/generator.py: move the common functionality from
  GeneratorIterator and Coroutine to the base class.  Review all
  calls to _PyGen_yf() in genobject.c.  This is needed before
  adding gi_yieldfrom/cr_await to generator/coroutines.  (Waiting
  because some work might be going on with raffael_t.)

* compare ``dir(posix)`` on py3.5 and cpython 3.5.

* review all unwrap_spec() that are meant to pass booleans (now
  with '=int').  Argument clinic turns these to PyObject_IsTrue(), i.e.
  accepting any object whatsoever(?!), which is supposedly a feature
  (see http://bugs.python.org/issue14705).

* ``math.isclose()``

* ``KeyError('pip.exceptions',) in weakref callback <function
  _get_module_lock.<locals>.cb at 0x00007f118e2c0020> ignored``
  we're getting them now on start-up, investigate

* ``print 5`` should give
  ``SyntaxError: Missing parentheses in call to 'print'``

* ``_utf8`` in W_UnicodeObject used to be quasi-immutable,
  document why it doesn't work and do a proper fix


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
