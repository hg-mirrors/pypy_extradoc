What would be cool to finish before the end of Milestone 2
==========================================================


In-progress ("Lock" section)
----------------------------


Misc stuff not formally in any milestone
----------------------------------------

* At some point, review lib-python/conftest.py to remove the skips
  due to deadlocks (search for "XXX:").
  update 1: some have been reenabled already! (richard 30.sept)
  update 2: most are gone (arigo 4 feb)

* collections.py: ``OrderedDict`` should again be a thin wrapper over
  ``dict``.  The main pain point is ``move_to_end(last=False)``.  See
  https://mail.python.org/pipermail/python-dev/2016-August/145837.html
  [DONE]

* compare ``dir(posix)`` on py3.5 and cpython 3.5.

* ``KeyError('pip.exceptions',) in weakref callback <function
  _get_module_lock.<locals>.cb at 0x00007f118e2c0020> ignored``
  we're getting them now on start-up, investigate

* Windows: issue 2310: kill WindowsError

* bytearray: 'del x[:10]' is now amortized constant-time (DONE)

* check that 'import array', say, finds and loads a file array.py,
  whereas 'import gc' does not ('gc' is a built-in module in CPython but
  'array' is typically an extension module; at least that's the case on
  Linux with default compilation settings).

* 'import stackless' fails

* "except pyopcode.Return:" in pyframe can't be there, because that's
  outside the JIT and it gives terrible performance (DONE)
  
* PEP 475: Retry system calls failing with EINTR (DONE)

* ast compiler: clean up POP_EXCEPT: either remove them, or use it to clean up
  the "finally: name = None; del name" nonsense at the end of any except block

* bonus: use all the features of _pypyjson from the json module again
  (eg c_encode_basestring_ascii)

* socket get lots of new methods (e.g. recvmsg, ...), all test stdlib tests
  are now skipping them

* _hashlib pbkdf2_hmac has a new 'fast' implemention in cpython,
  unsure if we are eager to implement that right now


Milestone 2 (end 2016, beginning 2017)
--------------------------------------

[Text from the proposal, please add progress in parentheses or square brackets]

Changes to the C API.

We get an up-to-date ``cpyext`` module that supports CPython 3.5 C
extension modules, including "argument clinic" and other parts of
the C API that are new.  The goal is that ``cpyext`` works as well
as it does on PyPy2.

Additionaly we resolve several security related issues found in CPython 3.4/3.5:

* Secure and interchangeable hash algorithm (PEP 456).
  [DONE, rpython-hash branch]

* New command line option for isolated mode.
  [I think it is already DONE]

* Enhancements to multiprocessing modules.

* HTTP cookie parsing is now stricter (issue 22796).
  [PURELY APP-LEVEL]

The measure of when this milestone is reached is based on the
following criteria: we can take a number of C extension modules that
work on CPython 3.5 (without reaching into the internals, like a few
modules do), and check that they work on PyPy 3.5 as well.  More
specifically, for any C module with a 2.7 version that works on PyPy
2.7, its 3.5 equivalent version must also work on PyPy 3.5.


Done not formally in the Milestone
----------------------------------

