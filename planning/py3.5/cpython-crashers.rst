CPython crashers
================

This document ways to crash CPython 3.5, or get completely unexpected
and undocumented results, or leak memory, etc.


* _PyGen_Finalize() should not fail with an exception
  http://bugs.python.org/issue27811

* PyFrameObject.f_gen can be left pointing to a dangling generator
  http://bugs.python.org/issue27812

* os.scandir() returns an iterable object that should not be used
  from multiple threads.  Doing so can e.g. cause one thread to
  close the dirp while another thread is still using it.  This is
  likely to crash.  Similarly, the test for (!iterator->dirp) at
  the start of ScandirIterator_iternext() is only done once even
  if the following loop runs two or three times because of "." or
  ".." entries.

* os.scandir() direntry objects should not have stat() called from two
  threads concurrently.  It will make two stat objects and leak one of
  them.

* _PyGen_yf() checks the opcode at [f_lasti + 1], which is the next
  opcode that will run when we resume the generator: either YIELD or
  YIELD_FROM.  But that is only true if the generator is not currently
  running.  If it is (which probably doesn't occur in reasonable Python
  code but can be constructed manually), then this checks for example
  the byte/word that describes the argument of the currently running
  opcode.  If we're very unlucky this byte has the value 72, which is
  YIELD_FROM.  Total nonsense and crashes follow.


Other bugs
----------

* on modern Linux: if the first call in the process to
  socketpair() ends in a EINVAL, then cpython will (possibly wrongly)
  assume it was caused by SOCK_CLOEXEC and not use SOCK_CLOEXEC at all
  in the future

* fcntl.ioctl(x, y, buf, mutate_flag): mutate_flag is there for the case
  of buf being a read-write buffer, which is then mutated in-place.
  But if we call with a read-only buffer, mutate_flag is ignored (instead
  of rejecting a True value)---ioctl(x, y, "foo", True) will not actually
  mutate the string "foo", but the True is completely ignored.

* re.sub(b'y', bytearray(b'a'), bytearray(b'xyz')) -> b'xaz'
  re.sub(b'y', bytearray(b'\\n'), bytearray(b'xyz')) -> internal TypeError
 
* not a bug: argument clinic turns the "bool" specifier into
  PyObject_IsTrue(), accepting any argument whatsoever.  This can easily
  get very confusing for the user, e.g. after messing up the number of
  arguments.  For example: os.symlink("/path1", "/path2", "/path3")
  doesn't fail, it just considers the 3rd argument as some true value.

* if you have a stack of generators where each is in 'yield from' from
  the next one, and you call '.next()' on the outermost, then it enters
  and leaves all intermediate frames.  This is costly but may be
  required to get the sys.settrace()/setprofile() hooks called.
  However, if you call '.throw()' or '.close()' instead, then it uses a
  much more efficient way to go from the outermost to the innermost
  frame---as a result, the enter/leave of the intermediate frames is not
  invoked.  This can confuse coverage tools and profilers.  For example,
  in a stack ``f1()->f2()->f3()``, vmprof would show f3() as usually
  called via f2() from f1() but occasionally called directly from f1().

* ceval.c: GET_AITER: calls _PyCoro_GetAwaitableIter(), which might
  get an exception from calling the user-defined __await__() or checking
  what it returns; such an exception is completely eaten.
