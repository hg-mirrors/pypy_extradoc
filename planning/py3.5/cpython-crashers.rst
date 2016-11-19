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
  opcode that will run when we resume the generator: either it is the
  opcode following the YIELD, or it is exactly YIELD_FROM.  It is not
  possible at the moment to write Python code that compiles to a YIELD
  immediately followed by YIELD_FROM, so by chance the two cases are
  correctly distinguished.  *However,* the discussion so far assumes
  that the generator is not currently running.  If it is (which probably
  doesn't occur in reasonable Python code but can be constructed
  manually), then this checks for example the byte/word that describes
  the argument of the currently running opcode.  If we're very unlucky
  this byte has the value 72, which is YIELD_FROM.  Total nonsense and
  crashes follow.

* faulthandler: register(): the signal handler, faulthandler_user(),
  changes errno in faulthandler_dump_traceback() but fails to restore it
  if chain=False.  This can rarely cause random nonsense in the main
  program.

* setting f_lineno didn't evolve when the rest of the bytecodes evolved,
  which means it is not safe any more::

    import sys

    def f():
        try:
            raise ValueError    # line 5
        except ValueError:
            print(42)           # line 7

    def my_trace(*args):
        print(args)
        if args[1] == 'line':
            f = args[0]
            if f.f_lineno == 5:
                f.f_lineno = 7
        return my_trace

    sys.settrace(my_trace)
    f()
    sys.settrace(None)


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
  mutate the string "foo", but the True is completely ignored.  (I think
  this is a bug introduced during the Argument Clinic refactoring.)

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

* this is an old issue that was forgotten twice on the
  issue tracker: ``class C: __new__=int.__new__`` and ``class C(int):
  __new__=object.__new__`` can each be instantiated, even though they
  shouldn't.  This is because ``__new__`` is completely ignored if it is
  set to any built-in function that uses ``tp_new_wrapper`` as its C code
  (many of the built-in types' ``__new__`` are like that).
  http://bugs.python.org/issue1694663#msg75957,
  http://bugs.python.org/issue5322#msg84112.  In (at least) CPython 3.5,
  a few classes work only thanks to abuse of this bug: for example,
  ``io.UnsupportedOperation.__new__(io.UnsupportedOperation)`` doesn't
  work, but that was not noticed because ``io.UnsupportedOperation()``
  mistakenly works.
 
* hash({}.values()) works (but hash({}.keys()) correctly gives
  TypeError).  That's a bit confusing and, as far as I can tell, always
  pointless.  Also, related: d.keys()==d.keys() but
  d.values()!=d.values().

* this program fails the check for no sys.exc_info(), even though at
  the point this assert runs (called from the <== line) we are not in
  any except/finally block.  This is a generalization of
  test_exceptions:test_generator_doesnt_retain_old_exc::

    import sys

    def g():
        try:
            raise ValueError
        except ValueError:
            yield 1
        assert sys.exc_info() == (None, None, None)
        yield 2

    gen = g()

    try:
        raise IndexError
    except IndexError:
        assert next(gen) is 1
    assert next(gen) is 2    # <==
