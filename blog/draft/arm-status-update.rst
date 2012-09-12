ARM Backend News Update
=======================

Starting with the good news, we finally merged the ``arm-backend-2`` branch
into the main development line. As described in previous posts the main goal of
this branch was to add support for ARM processors to PyPY's JIT.  As a general
byproduct the multi-architecture support should have tgo we improved several
details of PyPy to better support non-x86 architectures such as ARM and the
in-progress support for PPC64.  The JIT requires an ARMv7 or newer processor
with a VFP unit targeting the ARM application Profile. These are the same
requirements as those of the Ubuntu ARM port and correspond to the hardware
used in most smartphones and development boards offered today.
The non-JIT version
might support previous architecture versions, but will be slow.

Floating Point Support
----------------------
The JIT backends supports floating point numbers and therefore requires a VFP
unit to be present.  The **Procedure Call Standard for the ARM Architecture**
(`PDF`_) describes in the *base procedure call standard* how parameters are
passed in processor registers and on the stack when calling a function.

When supporting floating points there are two incompatible procedure call
standards and three ways of handling floats. Usually they are referred to as
*softfp*, *soft-float* and *hard-float*. The first two use the core registers
to pass floating point arguments. The first uses a software based
float-implementation, while the second can use a floating point unit. The
latter and incompatible one requires a floating point unit and uses the
coprocessor registers to pass floating arguments to calls. A detailed
comparison can be found `here`_.

The PyPy ARM backend currently supports the soft-float calling convention,
which is the most common one. This means that we have to copy floating point
values from the VFP to core registers and the stack when generating code for a
call that involves floating point values. Because the soft- and hard-float
calling conventions are incompatible, PyPy for ARM currently only will work on
systems built using soft-float.  More and more GNU/Linux distributions for ARM
are supporting hard-float. There is almost finished support in the JIT backend
for the hard-float calling convention, but we seem to have hit an issue with
ctypes/libffi on ARM that is blocking us to run our tests against the
hard-float implementation.


Testing and Infrastructure
--------------------------

By now we have an infrastructure the allows us to create cross-translated
binaries for ARM. Currently we compile binaries in a 32bit Ubuntu 12.04
environment using scratchbox2_ to encapsulate the cross-compiler calls. The
results can be downloaded and tested from our `nightly build server`_. Some
documentation on how to cross-translate is available in the `PyPy docs`_.

We also have some hardware to run the subset of the PyPy test-suite relevant to
the ARM-JIT backend and to run the tests suite that tests the translated ARM
binaries. The nightly tests are run on a Beagleboard-xM_ and an i.MX53_
versatile board (kindly provided by Michael Foord), both boards running the ARM port `Ubuntu
12.04 Precise Pangolin`_. The current results for the different builders can be
seen on the `PyPy buildbot`_. As can be seen there are still some issues to be
fixed.

.. _`PyPy buildbot`: http://buildbot.pypy.org/summary?branch=%3Ctrunk%3E&category=linux-armel
.. _`PyPy docs`: https://bitbucket.org/pypy/pypy/src/default/pypy/doc/arm.rst
.. _i.MX53: http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=IMX53QSB
.. _Beagleboard-xM: http://beagleboard.org/hardware-xm
.. _`Ubuntu 12.04 Precise Pangolin`: https://wiki.ubuntu.com/ARM 
.. _`scratchbox2`: http://maemo.gitorious.org/scratchbox2
.. _`nightly build server`: http://buildbot.pypy.org/nightly/trunk/
.. _`PDF`: http://infocenter.arm.com/help/topic/com.arm.doc.ihi0042d/IHI0042D_aapcs.pdf
.. _`here`: http://wiki.debian.org/ArmHardFloatPort/VfpComparison
