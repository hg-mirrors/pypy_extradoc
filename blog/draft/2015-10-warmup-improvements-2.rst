
Hello everyone!

This is the second part of the series of improvements in warmup time and
memory consumption in the PyPy JIT. This post covers recent work on sharing guard
resume data that was recently merged to trunk. It will be a part
of the next official PyPy release. To understand what it does, let's
start with a loop for a simple example::

   class A(object):
       def __init__(self, x, y):
           self.x = x
           self.y = y

       def call_method(self, z):
           return self.x + self.y + z

   def f():
       s = 0
       for i in range(100000):
           a = A(i, 1 + i)
           s += a.call_method(i)

At the entrance of the loop, we have the following set of operations:

    guard(i5 == 4)
    guard(p3 is null)
    p27 = getfield_gc_pure_r(p2, descr=<FieldP pypy.interpreter.pycode.PyCode.inst_co_cellvars 80>)
    p28 = getfield_gc_pure_r(p2, descr=<FieldP pypy.interpreter.pycode.PyCode.inst_co_freevars 128>)
    guard_class(p17, 4316866008, descr=<Guard0x104295e08>)
    p30 = getfield_gc_r(p17, descr=<FieldP pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_w_seq 16>)
    guard_nonnull(p30, descr=<Guard0x104295db0>)
    i31 = getfield_gc_i(p17, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
    p32 = getfield_gc_r(p30, descr=<FieldP pypy.objspace.std.listobject.W_ListObject.inst_strategy 16>)
    guard_class(p32, 4317041344, descr=<Guard0x104295d58>)
    p34 = getfield_gc_r(p30, descr=<FieldP pypy.objspace.std.listobject.W_ListObject.inst_lstorage 8>)
    i35 = getfield_gc_pure_i(p34, descr=<FieldS tuple1.item0 8>)

The above operations gets executed at the entrance, so each time we call ``f()``. They ensure
all the optimizations done below stay valid. Now, as long as nothing
crazy happens, they only ensure that the world around us never changed. However, if someone puts new
methods on class ``A``, any of the above guards might fail, despite the fact that it's a very unlikely
case, pypy needs to track how to recover from this situation. Each of those points needs to keep the full
state of the optimizations performed, so we can safely deoptimize them and reenter the interpreter.
This is vastly wasteful since most of those guards never fail, hence some sharing between guards
has been performed.

We went a step further - when two guards are next to each other or the
operations in between them are pure, we can safely redo the operations or to simply
put, resume in the previous guard. That means every now and again we execute a few
operations extra, but not storing extra info saves quite a bit of time and a bit of memory.
I've done some measurments on annotating & rtyping translation of pypy, which
is a pretty memory hungry program that compiles a fair bit. I measured, respectively:

* total time the translation step took (annotating or rtyping)

* time it took for tracing (that excludes backend time for the total JIT time) at
  the end of rtyping.

* memory the GC feels responsible for after the step. The real amount of memory
  consumed will always be larger and the coefficient of savings is in 1.5-2x mark

Here is the table:

+---------+-----------------+--------------+-------------------+----------------+--------------+
| branch  | time annotation | time rtyping | memory annotation | memory rtyping | tracing time |
+=========+=================+==============+===================+================+==============+
| default | 317s            | 454s         | 707M              | 1349M          | 60s          |
+---------+-----------------+--------------+-------------------+----------------+--------------+
| sharing | 302s            | 430s         | 595M              | 1070M          | 51s          |
+---------+-----------------+--------------+-------------------+----------------+--------------+
| win     | 4.8%            | 5.5%         | 19%               | 26%            | 17%          |
+---------+-----------------+--------------+-------------------+----------------+--------------+

Obviously pypy translation is an extreme example - the vast majority of the code out there
does not have that many lines of code to be jitted. However, it's at the very least
a good win for us :-)

We will continue to improve the warmup performance and keep you posted!

Cheers,
fijal
