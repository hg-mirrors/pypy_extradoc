
Hello everyone!

This is the second part of the series of improvement in warmup time and
memory consumption in the PyPy JIT. This post covers recent work on sharing guard
resume data that was recently merged to trunk. It will be a part
of the next official PyPy release. To understand what it does, let's
start with a loop for a simple example::

   def f():
       s = 0
       for i in range(100000):
          s += 1

which compiles to the following loop::

   label(p0, p1, p4, p6, p7, i39, i25, p15, p24, i44, i29, descr=TargetToken(4364727712))
   # check the loop exit
   i45 = i44 >= i29
   guard(i45 is false)
   # increase the loop counter
   i46 = i44 + 1
   # store the index into special W_RangeObject
   ((pypy.objspace.std.iterobject.W_AbstractSeqIterObject)p15).inst_index = i46
   # add s += 1 with overflow checking
   i47 = int_add_ovf(i39, 1)
   guard_no_overflow(descr=<Guard0x104295518>)
   guard_not_invalidated(descr=<Guard0x1042954c0>)
   i49 = getfield_raw_i(4336405536, descr=<FieldS pypysig_long_struct.c_value 0>)
   i50 = i49 < 0
   guard(i50 is false)
   jump(p0, p1, p4, p6, p7, i47, i44, p15, p24, i46, i29, descr=TargetToken(4364727712))

Now each ``guard`` needs a bit of data to know how to exit the compiled
assembler back up to the interpreter, and potentially to compile a bridge in the
future. Since over 90% of guards never fail, this is incredibly wasteful - we have a copy
of the resume data for each guard. When two guards are next to each other or the
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
