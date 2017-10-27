How to make your code 80 times faster
======================================

I often hear people who are happy because PyPy makes their code 2 times faster
or so. Here is a short personal story which shows PyPy can go well beyond
that.

**DISCLAIMER**: this is not a silver bullet or a general recipe: it worked in
this particular case, it might not work so well in other cases. But I think it
is still an interesting technique. Moreover, the various steps and
implementations are showed in the same order as I tried them during the
development, so it is a real-life example of how to proceed when optimizing
for PyPy.

Some months ago I `played a bit`_ with evolutionary algorithms: the ambitious
plan was to automatically evolve a logic which could control a (simulated)
quadcopter, i.e. a `PID controller`_ (**spoiler**: it doesn't fly).

.. _`played a bit`: https://github.com/antocuni/evolvingcopter
.. _`PID controller`: https://en.wikipedia.org/wiki/PID_controller

The idea is to have an initial population of random creatures: at each
generation, the ones with the best fitness survive and reproduce with small,
random variations.

However, for the scope of this post, the actual task at hand is not so
important, so let's jump straight to the code. To drive the quadcopter, a
``Creature`` has a ``run_step`` method which runs at each ``delta_t`` (`full
code`_)::

    class Creature(object):
        INPUTS = 2  # z_setpoint, current z position
        OUTPUTS = 1 # PWM for all 4 motors
        STATE_VARS = 1
        ...

        def run_step(self, inputs):
            # state: [state_vars ... inputs]
            # out_values: [state_vars, ... outputs]
            self.state[self.STATE_VARS:] = inputs
            out_values = np.dot(self.matrix, self.state) + self.constant
            self.state[:self.STATE_VARS] = out_values[:self.STATE_VARS]
            outputs = out_values[self.STATE_VARS:]
            return outputs
      
- ``inputs`` is a numpy array containing the desired setpoint and the current
  position on the Z axis;

- ``outputs`` is a numpy array containing the thrust to give to the motors. To
  start easy, all the 4 motors are constrained to have the same thrust, so
  that the quadcopter only travels up and down the Z axis;

- ``self.state`` contains arbitrary values of unknown size which are passed from
  one step to the next;

- ``self.matrix`` and ``self.constant`` contains the actual logic. By putting
  the "right" values there, in theory we could get a perfectly tuned PID
  controller. These are randomly mutated between generations.

.. _`full code`: https://github.com/antocuni/evolvingcopter/blob/master/ev/creature.py

``run_step`` is run at 100Hz (in the virtual time frame of the simulation). At each
generation, we test 500 creatures for a total of 12 virtual seconds each. So,
we have a total of 600,000 executions of ``run_step`` at each generation.

At first, I simply tried to run this code on CPython; here is the result::

    $ python -m ev.main
    Generation   1: ... [population = 500]  [12.06 secs]
    Generation   2: ... [population = 500]  [6.13 secs]
    Generation   3: ... [population = 500]  [6.11 secs]
    Generation   4: ... [population = 500]  [6.09 secs]
    Generation   5: ... [population = 500]  [6.18 secs]
    Generation   6: ... [population = 500]  [6.26 secs]

Which means ~6.15 seconds/generation, excluding the first.

Then I tried with PyPy 5.9::

    $ pypy -m ev.main
    Generation   1: ... [population = 500]  [63.90 secs]
    Generation   2: ... [population = 500]  [33.92 secs]
    Generation   3: ... [population = 500]  [34.21 secs]
    Generation   4: ... [population = 500]  [33.75 secs]

Ouch! We are ~5.5x slower than CPython. This was kind of expected: numpy is
based on cpyext, which is infamously slow (although `we are working on that`_).

So, let's try to avoid cpyext. The first obvious step is to use numpypy_
instead of numpy (actually, there a hack_ to use just the micronumpy
part). Let's see if the speed improves::

    $ pypy -m ev.main   # using numpypy
    Generation   1: ... [population = 500]  [5.60 secs]
    Generation   2: ... [population = 500]  [2.90 secs]
    Generation   3: ... [population = 500]  [2.78 secs]
    Generation   4: ... [population = 500]  [2.69 secs]
    Generation   5: ... [population = 500]  [2.72 secs]
    Generation   6: ... [population = 500]  [2.73 secs]

So, ~2.7 seconds on average: this is 12x faster than PyPy+numpy, and more than
2x faster than the original CPython. At this point, most people would be happy
and go tweeting how PyPy is great.

.. _`we are working on that`: https://morepypy.blogspot.it/2017/10/cape-of-good-hope-for-pypy-hello-from.html
.. _numpypy: http://doc.pypy.org/en/latest/faq.html#what-about-numpy-numpypy-micronumpy
.. _hack: https://github.com/antocuni/evolvingcopter/blob/master/ev/pypycompat.py

In general, when talking of CPython vs PyPy, I am rarely satified of a 2x
speedup: I know that PyPy can do much better than this, especially if you
write code which is specifically optimized for the JIT. For a real-life
example, have a look at `capnpy benchmarks`_, in which the PyPy version is
~15x faster than the heavily optimized CPython+Cython version (both have been
written by me, and I tried hard to write the fastest code for both
implementations).

.. _`capnpy benchmarks`: http://capnpy.readthedocs.io/en/latest/benchmarks.html

So, let's try to do better. As usual, the first thing to do is to profile and
see where we spend most of the time. Here is the `vmprof profile`_. We spend a
lot of time inside the internals of numpypy, and allocating tons of temporary
arrays to store the results of the various operations.

Also, let's look at the `jit traces`_ and search for the function ``run``:
this is loop in which we spend most of the time, and it is composed 
of 1796 operations.  The operations emitted for the line ``np.dot(...) +
self.constant`` are listed between lines 1217 and 1456; 239 low level
operations are a lot. If we look at them, we can see for example that there is
a call to the RPython function `descr_dot`_, at line 1232. But there are also
calls to ``raw_malloc``, at line 1295, which allocates the space to store the
result of ``... + self.constant``.

.. _`vmprof profile`: http://vmprof.com/#/449ca8ee-3ab2-49d4-b6f0-9099987e9000
.. _`jit traces`: http://vmprof.com/#/28fd6e8f-f103-4bf4-a76a-4b65dbd637f4/traces
.. _`descr_dot`: https://bitbucket.org/pypy/pypy/src/89d1f31fabc86778cfaa1034b1102887c063de66/pypy/module/micronumpy/ndarray.py?at=default&fileviewer=file-view-default#ndarray.py-1168

All of this is very suboptimal: in this particular case, we know that the
shape of ``self.matrix`` is always ``(3, 2)``: so, we are doing an incredible
amount of work. We also use ``malloc()`` to create a temporary array just to call an RPython
function which ultimately does a total of 6 multiplications and 8 additions.

One possible solution to this nonsense is a well known compiler optimization:
loop unrolling.  From the compiler point of view, unrolling the loop is always
risky because if the matrix is too big you might end up emitting a huge blob
of code, possibly uselss if the shape of the matrices change frequently: this
is the main reason why the PyPy JIT does not even try to do it in this case.

However, we **know** that the matrix is small, and always of the same
shape. So, let's unroll the loop manually::

    class SpecializedCreature(Creature):

        def __init__(self, *args, **kwargs):
            Creature.__init__(self, *args, **kwargs)
            # store the data in a plain Python list, which pypy is able to
            # optimize as a float array
            self.data = list(self.matrix.ravel()) + list(self.constant)
            self.data_state = [0.0]
            assert self.matrix.shape == (2, 3)
            assert len(self.data) == 8

        def run_step(self, inputs):
            # state: [state_vars ... inputs]
            # out_values: [state_vars, ... outputs]
            k0, k1, k2, q0, q1, q2, c0, c1 = self.data
            s0 = self.data_state[0]
            z_sp, z = inputs
            #
            # compute the output
            out0 = s0*k0 + z_sp*k1 + z*k2 + c0
            out1 = s0*q0 + z_sp*q1 + z*q2 + c1
            #
            self.data_state[0] = out0
            outputs = [out1]
            return outputs

In the `actual code`_ there is also a sanity check which asserts that the
computed output is the very same as the one returned by ``Creature.run_step``.

Note that is code is particularly PyPy-friendly. Thanks to PyPy's `list strategies`_
optimizations, ``self.data`` as a simple list of floats is internally represented
as a flat array of C doubles, i.e. very fast and compact.

.. _`actual code`: https://github.com/antocuni/evolvingcopter/blob/master/ev/creature.py#L100
.. _`list strategies`: https://morepypy.blogspot.it/2011/10/more-compact-lists-with-list-strategies.html

So, let's try to see how it performs. First, with CPython::

    $ python -m ev.main
    Generation   1: ... [population = 500]  [7.61 secs]
    Generation   2: ... [population = 500]  [3.96 secs]
    Generation   3: ... [population = 500]  [3.79 secs]
    Generation   4: ... [population = 500]  [3.74 secs]
    Generation   5: ... [population = 500]  [3.84 secs]
    Generation   6: ... [population = 500]  [3.69 secs]

This looks good: 60% faster than the original CPython+numpy
implementation. Let's try on PyPy::

    Generation   1: ... [population = 500]  [0.39 secs]
    Generation   2: ... [population = 500]  [0.10 secs]
    Generation   3: ... [population = 500]  [0.11 secs]
    Generation   4: ... [population = 500]  [0.09 secs]
    Generation   5: ... [population = 500]  [0.08 secs]
    Generation   6: ... [population = 500]  [0.12 secs]
    Generation   7: ... [population = 500]  [0.09 secs]
    Generation   8: ... [population = 500]  [0.08 secs]
    Generation   9: ... [population = 500]  [0.08 secs]
    Generation  10: ... [population = 500]  [0.08 secs]
    Generation  11: ... [population = 500]  [0.08 secs]
    Generation  12: ... [population = 500]  [0.07 secs]
    Generation  13: ... [population = 500]  [0.07 secs]
    Generation  14: ... [population = 500]  [0.08 secs]
    Generation  15: ... [population = 500]  [0.07 secs]

Yes, it's not an error. After a couple of generations, it stabilizes at around
~0.07-0.08 seconds per generation. This is around **80 (eighty) times faster**
than the original CPython+numpy implementation, and around 35-40x faster than
the naive PyPy+numpypy one.

Let's look at the trace_ again: it no longer contains expensive calls, and
certainly no more temporary ``malloc()`` s. The core of the logic is between
lines 386-416, where we can see that it does fast C-level multiplications and
additions: ``float_mul`` and ``float_add`` are translated straight into
``mulsd`` and ``addsd`` x86 instructions.

.. _trace: http://vmprof.com/#/402af746-2966-4403-a61d-93015abac033/traces

As I said before, this is a very particular example, and the techniques
described here do not always apply: it is not realistic to expect an 80x
speedup, unfortunately. However, it clearly shows the potential of PyPy when
it comes to high-speed computing. And most importantly, it's not a toy
benchmark which was designed specifically to have good performance on PyPy:
it's a real world example, albeit small.

You might be also interested in the talk I gave at last EuroPython, in which I
talk about a similar topic: "The Joy of PyPy JIT: abstractions for free"
(abstract_, slides_ and video_).

.. _abstract: https://ep2017.europython.eu/conference/talks/the-joy-of-pypy-jit-abstractions-for-free
.. _slides: https://speakerdeck.com/antocuni/the-joy-of-pypy-jit-abstractions-for-free
.. _video: https://www.youtube.com/watch?v=NQfpHQII2cU
