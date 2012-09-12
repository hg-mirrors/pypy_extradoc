ARM Backend News Update
=======================

Starting with the good news, we finally merged the ``arm-backend-2`` branch
into PyPy's main development line. As described in previous_ posts_ the main
goal of this branch was to add support for ARM processors to PyPY's JIT.  As a
general byproduct PyPy should now do a better job supporting non-x86
architectures such as ARM and the in-progress support for PPC64.

On ARM, the JIT requires an ARMv7 processor or newer with a VFP unit targeting
the ARM application profile. Although this sounds like a strong restriction,
most of the ARM processors used in mobile devices and development boards are
ARMv7 (sadly the raspberry pi isn't) or newer. Also these are the same
requirements as those of the Ubuntu ARM port. The non-JIT version might support
previous architecture versions, but without the JIT it will be slow.


Floating Point Support
----------------------

The support for a floating point unit is optional for ARM processor vendors.
Due to this there are different calling conventions, that differ on the
requirement for a floating point unit and the treatment of floats.
The **Procedure Call Standard for the ARM Architecture**
(`PDF`_) describes in the *base procedure call standard* how parameters are
passed in processor registers and on the stack when calling a function.

When adding floating points to the mix there are two incompatible procedure
call standards and three ways of handling floats. Usually they are referred to
as *softfp*, *soft-float* and *hard-float*. The first two use the core
registers to pass floating point arguments and do not make any assumptions
about a floating point unit. The first uses a software based
float-implementation, while the second can use a floating point unit. The
latter and incompatible one requires a floating point unit and uses the
coprocessor registers to pass floating arguments to calls. A detailed
comparison can be found `here`_.

At the time we started implementing the float support in the ARM backend of the
JIT, the soft-float calling conventions were the most commonly supported ones
by most GNU/Linux distributions, so we decided to implement that one first.
This means that we have to copy floating point values from the VFP to core
registers and the stack when generating code for a call that involves floating
point values. Because the soft- and hard-float calling conventions are
incompatible, PyPy for ARM currently will only work on systems built using
soft-float.  By now more and more GNU/Linux distributions for ARM are
supporting hard-floats.  In PyPy there is basic support in the JIT backend for
the hard-float calling convention. But we seem to have hit an issue with
ctypes/libffi on ARM that is blocking us to run our tests against the
hard-float implementation.


Testing and Infrastructure
--------------------------

By now we have an infrastructure the allows us to create cross-translated
binaries for ARM and to run tests on them. Currently we compile binaries in a
32bit Ubuntu 12.04 environment using scratchbox2_ to encapsulate the
cross-compiler calls. The results can be downloaded and tested from our
`nightly build server`_. Some documentation on how to cross-translate is
available in the `PyPy docs`_.

We also have some hardware to run the subset of the PyPy test-suite relevant to
the ARM-JIT backend and to run the tests suite that tests the translated ARM
binaries. The nightly tests are run on a Beagleboard-xM_ and an i.MX53_
versatile board (kindly provided by Michael Foord), both boards run the ARM port `Ubuntu
12.04 Precise Pangolin`_. The current results for the different builders can be
seen on the `PyPy buildbot`_. As can be seen there are still some issues to be
fixed, but we are getting there.


Open Topics
-----------
In a previous post we mentioned a set of open topics regarding PyPy's ARM
support, here is an update on these topics:

Done:

* We are looking for a better way to translate PyPy for ARM, than the one
  describe above. I am not sure if there currently is hardware with enough
  memory to directly translate PyPy on an ARM based system, this would require
  between 1.5 or 2 Gig of memory. A fully QEMU based approach could also work,
  instead of Scratchbox2 that uses QEMU under the hood.  *The scratchbox2 based
  approach has given the best results so far. Qemu has shown to be too unstable
  to be used as a base for the translation, also the qemu-arm emulation is very
  slow when compared to cross-translating.*
* Test the JIT on different hardware.
  *As mentioned we are running nightly tests on a Beagleboard-xM and a i.MX53 board.*
* Continuous integration: We are looking for a way to run the PyPy test suite
  to make sure everything works as expected on ARM, here QEMU also might
  provide an alternative.  
  *As stated above this is now working, we explored
  using qemu-arm and a chroot to run tests. This, although faster than
  our boards, was very unstable and crashed randomly making it unusable to run tests on
  a regular basis. A fully emulated approach using QEMU might still be worth trying.*
* Improve the tools, i.e. integrate with jitviewer_.

Long term on open topics/projects for ARM:

* Review of the generated machine code the JIT generates on ARM to see if the
  instruction selection makes sense for ARM.
* Build a version that runs on Android.
* Experiment with the JIT settings to find the optimal thresholds for ARM.
  This is still open
* A long term plan would be to port the backend to ARMv5 ISA and improve the
  support for systems without a floating point unit. This would require to
  implement the ISA and create different code paths and improve the instruction
  selection depending on the target architecture.

While we continue to fix the remaining issues you can get a nightly version to
try PyPy on ARM.


.. _Beagleboard-xM: http://beagleboard.org/hardware-xm
.. _`PDF`: http://infocenter.arm.com/help/topic/com.arm.doc.ihi0042d/IHI0042D_aapcs.pdf
.. _`PyPy buildbot`: http://buildbot.pypy.org/summary?branch=%3Ctrunk%3E&category=linux-armel
.. _`PyPy docs`: https://bitbucket.org/pypy/pypy/src/default/pypy/doc/arm.rst
.. _`Ubuntu 12.04 Precise Pangolin`: https://wiki.ubuntu.com/ARM 
.. _`here`: http://wiki.debian.org/ArmHardFloatPort/VfpComparison
.. _`nightly build server`: http://buildbot.pypy.org/nightly/trunk/
.. _`scratchbox2`: http://maemo.gitorious.org/scratchbox2
.. _i.MX53: http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=IMX53QSB
.. _jitviewer: https://bitbucket.org/pypy/jitviewer
.. _posts: http://morepypy.blogspot.de/2012/02/almost-there-pypys-arm-backend_01.html
.. _previous: http://morepypy.blogspot.de/2011/01/jit-backend-for-arm-processors.html
