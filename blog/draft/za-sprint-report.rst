Hello.

We're about to finish a PyPy sprint in Cape Town, South Africa that was
one of the smallest done so far, only having Armin Rigo and Maciej Fijalkowski
with Alex Gaynor joining briefly at the beginning, however also one of the
longest, lasting almost 3 weeks. The sprint theme seems to be predominantly
"no new features" and "spring cleaning". We overall removed about 20k lines
of code in the PyPy source tree. The breakdown of things done and worked on:

* We killed `SomeObject` support in annotation and rtyper. This is a modest
  code saving, however, it reduces the complexity of RPython and also,
  hopefully, improves compile errors from RPython. We're far from done
  on the path to have comprehensible compile-time errors, but the first
  step is always the hardest :)

* We killed some magic in specifying the interface between builtin functions
  and Python code. It used to be possible to write builtin functions like this::

    def f(space, w_x='xyz'):

  which will magically wrap `'xyz'` into a W_StringObject. Right now, instead,
  you have to write::

    @unwrap_spec(w_x=WrappedDefault('xyz'))
    def f(space, w_x):

  which is more verbose, but less magical.

* We killed the `CExtModuleBuilder` which is the last remaining part of
  infamous extension compiler that could in theory build C extensions
  for CPython in RPython. This was never working very well and the main
  part was killed long ago.

* We killed various code duplications in the C backend.

* We killed `microbench` and a bunch of other small-to-medium unused
  directories.

* We killed llgraph JIT backend and rewrote it from scratch. Now the llgraph
  backend is not translatable, but this feature was rarely used and caused
  a great deal of complexity.

* We progressed on `continulet-jit-3` branch, up to the point of merging
  it into `result-in-resops` branch, which also has seen a bit of progress.

  Purpose of those two branches:

  * `continulet-jit-3`: enable stackless to interact with the JIT by killing
    global state while resuming from the JIT into the interpreter. This has
    multiple benefits. For example it's one of the stones on the path to
    enable STM for PyPy. It also opens new possibilities for other optimizations
    including Python-Python calls and generators.

  * `result-in-resops`: the main goal is to speed up the tracing time of PyPy.
    We found out the majority of time is spent in the optimizer chain,
    which faces an almost complete rewrite. It also simplifies the storage
    of the operations as well as the number of implicit invariants that have
    to be kept in mind while developing.

* We finished and merged the excellent work by Ronan Lamy which makes the
  flow object space (used for abstract interpretation during RPython
  compilation) independent from the Python interpreter. This means
  we've achieved an important milestone on the path of separating the RPython
  translation toolchain from the PyPy Python interpreter.

Cheers,
fijal & armin

  
  
