Primitive objects and object identity
=====================================

Hi all,

Recently PyPy merged a pretty big branch that allows for transparently
type-specializing dictionaries. That means if you write something like::

    strs = {x: str(x) for x in xrange(100000)}

The dictionary would be specialized for integer keys, obviating the need to
allocate W_IntObjects (PyPy's equivilant to PyInt_Object).

This, however introduces interesting behavior surrounding object identity
(*only* with respect to primitive objects, none of what is discussed affects
either mutable, or user-defined objects), specifically the follow code no
longer works::

    x = int(x)
    z = {x: None}
    assert next(iter(z)) is x

This would similiarly fail if you replaced is with comparing the id()s. The
question now is, is this behavior a violation of the Python language
definition, or is it a legal, interpreter defined difference?

There are several arguments in favor:

1) It is easier to implement this way, and removes complexity in the
   interpreter implementation, and allows for better performance.

2) For all of these objects, identity is trivial. That is to say identity could
   always be replacement by an equality test and no semantics would be voilated.
   In that respect requiring that identity be maintained adds no value, the
   new object is completely indistinguishable

3) A reliance on object identity leads to some rather strange behavior, a good
   example of this is a recent discussion about the identity shortcut in
   ``dict.__contains__`` and ``list.__contains__``, specifically in the case of
   ``nan``. At present if you have a ``dict`` with a ``nan`` key the only way
   to retreive that value is to use the exact same ``nan`` object, another one
   will not do because ``nan`` does not have reflexive identity. Even on
   CPython, passing around this object could easily lose it's identity, for
   example various functions in the ``math`` module return a ``nan`` given a
   ``nan`` argument, but they make no guarntee that they return the same
   instance, furthering a reliance on any such behavior is wrong, given that
   equality is always a valid substitute.

And arguments against::

1) It may break some existing code (so far the only such code I've found is in
   the Python test suite, it was not testing this behavior directly, but rather
   incidentally relied on it).


I can find no other argument against it.

Note that should we decide that this is in fact a violation of the language
spec, the resulting behavior in PyPy will be for identity to be equality on
primitive type objects.  That is to say, the following code would work::

    assert all([
        x is (x + 1 - 1)
        for x in xrange(sys.minint, sys.maxint)
    ])

As actually assigning allocating W_IntObjects will not occur.

Opinionig welcome,
Alex
