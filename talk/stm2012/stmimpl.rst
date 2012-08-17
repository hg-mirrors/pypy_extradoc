========================
STM implementation model
========================

Overview
--------

Objects are either global (visible to everybody, and read-only), or
they are local (visible only to the current thread).

Objects start by being local: when a thread allocates new objects, they
are not visible to other threads until a commit occurs.  When the commit
occurs, the surviving local objects become global.

Once an object is global, its content never changes any more: only parts
of the object header can be updated by the STM mechanisms.

If a following transaction modifies a global object, the changes are
done in a local copy.  If this transaction successfully commits, the
original global object is *not* changed --- it is really immutable.  But
the copy becomes global, and the old global object's header is updated
with a pointer to the new global object.


CPUs model
----------

For our purposes the following simplified model is enough (x86 only):
every CPU's load instructions get the current value from the main memory
(the cache is transparent).  However, a CPU's store instructions might
be delayed and only show up later in main memory.  The delayed stores
are always flushed to main memory in program order.

Of course if the same CPU loads a value just stored, it will see the
value as modified (self-consistency); but other CPUs might temporarily
still see the old value.

The MFENCE instruction waits until all delayed stores from this CPU have
been flushed.  (A CPU has no built-in way to wait until *other* CPU's
stores are flushed.)

The LOCK CMPXCHG instruction does a MFENCE followed by an atomic
compare-and-exchange operation.


Object header
-------------

Every object starts with three fields:

- h_global (boolean)
- h_nonmodified (boolean)
- h_version (unsigned integer)

The h_version is an unsigned "version number".  More about it below.
The other two fields are flags.  (In practice they are just two bits
of the GC h_tid field.)


Transaction details
-------------------

Every CPU is either running one transaction, or is busy trying to commit
the transaction it has so far.  The following data is transaction-local:

- start_time
- global2local

The ``start_time`` is the "time" at which the transaction started.  All
reads and writes done so far in the transaction appear consistent with
the state at time ``start_time``.  The "time" is a single global number
that is atomically incremented whenever a transaction commits.

``global2local`` is a dictionary-like mapping of global objects to their
corresponding local objects.


Pseudo-code during transactions
---------------------------------------

Variable names:

* ``P`` is a pointer to any object.

* ``G`` is a pointer to a *global* object.

* ``R`` is a pointer to an object that was checked for being
  *read-ready*: reading its fields is ok.

* ``L`` is a pointer to a *local* object.  Reading its fields is
  always ok, but not necessarily writing.

* ``W`` is a pointer to a local object ready to *write*.


``W = Allocate(size)`` allocates a local object, and as the name of
the variable suggests, returns it ready to write::

    def Allocate(size):
        W = malloc(size)
        W->h_global = False
        W->h_nonmodified = False
        W->h_version = 0
        return W


``R = LatestGlobalVersion(G)`` takes a pointer ``G`` to a global object,
and if necessary follows the chain of newer versions, until it reaches
the most recent version ``R``.  Then it checks the version number of
``R`` to see that it was not created after ``start_time``.
Pseudo-code::

    def LatestGlobalVersion(G):
        R = G
        while (v := R->h_version) & 1:    # "has a more recent version"
            R = v & ~ 1
        if v > start_time:                # object too recent?
            validate_fast()               # try to move start_time forward
            return LatestGlobalVersion(G) # restart searching from G
        PossiblyUpdateChain(G)
        return R


``R = DirectReadBarrier(P)`` is the first version of the read barrier.
It takes a random pointer ``P`` and returns a possibly different pointer
``R`` out of which we can read from the object.  The result ``R``
remains valid for read access until either the current transaction ends,
or until a write into the same object is done.

::

    def DirectReadBarrier(P):
        if not P->h_global:         # fast-path
            return P
        R = LatestGlobalVersion(P)
        if R in global2local:
            L = global2local[R]
            return L
        else:
            AddInReadSet(R)         # see below
            return R


``L = Localize(R)`` is an operation that takes a read-ready pointer to
a global object and returns a corresponding pointer to a local object.

::

    def Localize(R):
        if P in global2local:
            return global2local[P]
        L = malloc(sizeof R)
        L->h_nonmodified = True
        L->h_version = P
        L->objectbody... = R->objectbody...
        global2local[R] = L
        return L


``L = LocalizeReadBarrier(P)`` is a different version of the read
barrier that works by returning a local object.

::

    def LocalizeReadBarrier(P):
        if not P->h_global:       # fast-path
            return P
        R = LatestGlobalVersion(P)
        L = Localize(R)
        return L


``W = WriteBarrier(P)`` is the write barrier.

::

    def WriteBarrier(P):
        W = LocalizeReadBarrier(P)
        W->h_nonmodified = False
        return W


``R = AdaptiveReadBarrier(P)`` is the adaptive read barrier.  It can use
the technique of either ``DirectReadBarrier`` or
``LocalizeReadBarrier``, based on heuristics for better performance::

    def AdaptiveReadBarrier(P):
        if not P->h_global:       # fast-path
            return P
        R = LatestGlobalVersion(P)
        if R in global2local:
            return global2local[R]
        if R seen often enough in readset:
            L = Localize(R)       # LocalizeReadBarrier
            return L
        else:
            AddInReadSet(R)       # DirectReadBarrier
            return R


This adaptive localization of read-only objects is useful for example in
the following situation: we have a pointer ``P1`` to some parent object,
out of which we repeatedly try to read the same field ``Field`` and use
the result ``P`` in some call.  Because the call may possibly have write
effects to the parent object, we normally need to redo
``DirectReadBarrier`` on ``P1`` every time.  If instead we do
``AdaptiveReadBarrier`` then after a few iterations it will localize the
object and return ``L1``.  On ``L1`` no read barrier is needed any more.

Moreover, if we also need to read the subobject ``P``, we also need to
call a read barrier on it every time.  It may return ``L`` after a few
iterations, but this time we win less, because during the next iteration
we again read ``P`` out of ``L1``.  The trick is that when we read a
field out of a local object ``L1``, and it is a pointer on which we
subsequently do a read barrier, then afterwards we can update the
original pointer directly in ``L1``.

Similarily, if we start with a global ``R1`` and read a pointer ``P``
which is updated to its latest global version ``R``, then we can update
the original pointer in-place.

The only case in which it is not permitted xxx

::

    def DependentUpdate(R1, Field, R):
        if R1->h_global:     # can't modify R1 unless it is local
            return
        R1->Field = R        # possibly update the pointer


