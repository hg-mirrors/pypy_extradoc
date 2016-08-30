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
