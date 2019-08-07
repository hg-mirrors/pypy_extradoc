Hi all,

Anvil_ is a UK-based company sponsoring one month of work to revive PyPy's
"sandbox" mode and upgrade it to PyPy3.  Thanks to them, sandboxing will be
given a second life!

Remember sandboxing_?  It is (or rather was) a special version of PyPy that runs
in a fully-isolated mode.  It gives a safe way to execute arbitrary Python
scripts (*whole* scripts, not small bits of code inside your larger Python
program).  Such scripts can be fully untrusted, and they can try to do
anything---there are no syntax-based restrictions, for example---but whatever
they do, any communication with the external world is not actually done but
delegated to the parent process.  This is similar but much more flexible than
Linux's Seccomp approach, and it is more lightweight than setting up a full
virtual machine.  It also works without operating system support.

This sandbox mode of PyPy was deprecated long ago because of a lack of
interest, and because it took too much effort for us to maintain it.

Now we have found that we have an actual user, Anvil_.  As far as I can tell
they are still using a very old version of PyPy, the last one that supported
sandboxing.  Thus this contract to modernize it and port it to PyPy3.

Part of my motivation for accepting this work is that I may have found a way to
tweak the protocol on the pipe between the sandboxed PyPy and the parent
controller process.  This should make the sandboxed PyPy more resilient against
future developments; at most, in the future some tweaks will be needed in the
controller process but hopefully not deep inside the guts of the sandboxed
PyPy.  Among the advantages, such a more robust solution should mean that we
can actually get a working sandboxed PyPy or sandboxed PyPy3 or sandboxed
version of any other interpreter written in RPython---with just an extra
argument when calling ``rpython`` to translate this interpreter.  If everything
works as planned, sandboxing may be given a second life.

Armin Rigo

.. _Anvil: https://anvil.works
.. _sandboxing: http://doc.pypy.org/en/latest/sandbox.html
