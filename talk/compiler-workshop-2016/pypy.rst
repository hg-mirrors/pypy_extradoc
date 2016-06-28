PyPy - DRAFT
============

A quick overview of PyPy for other Python-compiler developers


What is Our Niche
-----------------

PyPy is a mature production-ready framework automatically speeding up pure
python code by factors of 2-5 in commercial settings.

What We Bring to the Table
--------------------------

Our core is based on cutting-edge JIT compiler
research, written in Python. Being written in Python means we can quickly
try out (and reject or incorporate) new ideas. For instance, our STM work has
uncovered subtle bugs in CLANG and GCC, or the fact that we can easily try out
new register allocation strategies.

What We Need Help With
----------------------

We seem to be more successful in improving core technologies than creating a
end-user friendly nicely packaged distribution. We are also extremely
under-funded. For instance, we could be doing alot more for data science but
are moving slowly forward on a volunteer basis with C-API compatibility.

