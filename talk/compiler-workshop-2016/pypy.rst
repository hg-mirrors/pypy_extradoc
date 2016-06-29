PyPy - DRAFT
============

A quick overview of PyPy for other Python-compiler developers

What is Our Niche
-----------------

PyPy is a mature production-ready framework automatically speeding up pure
python code by factors of 2-5 in commercial settings.

The PyPy community offers several tools to inspect and optimize Python programs.
Examples: vmprof, cffi

What We Bring to the Table
--------------------------

Our core is based on cutting-edge JIT compiler
research, written in Python. Being written in Python means we can quickly
try out (and reject or incorporate) new ideas. For instance, our STM work has
uncovered subtle bugs in CLANG and GCC, or the fact that we can easily try out
new register allocation strategies.

Our JIT is not only advanced, but runs on all major platforms (Linux, Windows, MacOS, ...) including
four different CPU architectures (x86, arm, ppc, s390x).

We have built a high level language to aid the construction of VMs (called *RPython*)
It imports the complete program
Flow graphs -> Annotation -> RTyping -> Code generation

Advantages:
* Whole program optimizations (take that C)
* Deliver features fast, without sacrificing speed
* Loosely coupled (JIT, Interp., RPython)

Downsides:
* Takes a while to translate

What We Need Help With
----------------------

We seem to be more successful in improving core technologies than creating a
end-user friendly nicely packaged distribution. We are also extremely
under-funded. For instance, we could be doing alot more for data science but
are moving slowly forward on a volunteer basis with C-API compatibility.

Our interests lie in still providing the confort of the Python eco system,
but not sacrificing execution time. Some details (e.g. garbage collection scheme)
have some impact on user programs. We could use a lot more help in identifying and resolving
some of these issues. If programs do not run out of the box, most users will stick to CPython
because their performance problems are not that of an issue (at that point in time).
If we could resolve those issues (funded, or externally contributed) we would create a much
better user experience.

We are also working on Micro NumPy, which provides the kernels for numerical operations.
It is very much complete, but still some features are missing. We would love to have a
partner/company that would help us to complete NumPy for PyPy.

We are open to changes to our JIT scheme. We are working on both high level optimizations and
backend oriented changes. Ideas would be to mitigate some issues with our tracing JIT compiler
(or even build a region based compiler) and many more. Most of these aspects are covered quite well by
our core development team, but we will eventually take another big step in near future towards the 7th version
of our JIT.

Other Interesting Aspects
-------------------------

(Backup slides)

Some words about how our JIT compiler works?

We sprint 2-3 times a year (open to the public).
