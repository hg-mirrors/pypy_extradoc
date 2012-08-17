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
with a pointer to the new global object.  We thus make a chained list
of global versions.

It is the job of the GC to collect the older versions when they are
not referenced any more by any thread.


CPUs model
----------

For our purposes the following simplified model is enough (x86 only):
every CPU's load instructions get the current value from the main memory
(the cache is transparent).  However, a CPU's store instructions might
be delayed and only show up later in main memory.  The delayed stores
are always flushed to main memory in program order.

Of course if the same CPU loads a value it just stored, it will see the
value as modified (self-consistency); but other CPUs might temporarily
see the old value.

The MFENCE instruction waits until all delayed stores from this CPU have
been flushed.  (A CPU has no built-in way to wait until *other* CPUs'
stores are flushed.)

The LOCK CMPXCHG instruction does a MFENCE followed by an atomic
compare-and-exchange operation.


Object header
-------------

Every object starts with three fields:

- h_global (boolean)
- h_possibly_outdated (boolean)
- h_written (boolean)
- h_version (unsigned integer)

The h_version is an unsigned "version number".  More about it below.
The other fields are flags.  (In practice they are just bits inside the
GC h_tid field.)

- ``h_global`` means that the object is a global object.

- ``h_possibly_outdated`` is used as an optimization: it means that the
  object is possibly outdated.  It is False for all local objects.  It
  is also False if the object is a global object, is the most recent of
  its chained list of versions, and is known to have no modified local
  version in any transaction.

- ``h_written`` is set on local objects that have been written to.


Transaction details
-------------------

Every CPU is either running one transaction, or is busy trying to commit
the transaction it has so far.  The following data is transaction-local:

- start_time
- global_to_local
- list_of_read_objects
- recent_reads_cache

The ``start_time`` is the "time" at which the transaction started.  All
reads and writes done so far in the transaction appear consistent with
the state at time ``start_time``.  The "time" is a single global number
that is atomically incremented whenever a transaction commits.

``global_to_local`` is a dictionary-like mapping of global objects to
their corresponding local objects.

``list_of_read_objects`` is a set of all global objects read from, in
the version that was used for reading.  It is actually implemented as a
list, but the order or repeated presence of elements in the list is
irrelevant.

``recent_reads_cache`` is a fixed-size cache that remembers recent
additions to the preceeding list, in order to avoid inserting too much
repeated entries into the list, as well as keep lightweight statistics.


Pseudo-code: read/write barriers
---------------------------------------

Variable names:

* ``P`` is a pointer to any object.

* ``G`` is a pointer to a *global* object.

* ``R`` is a pointer to an object that was checked for being
  *read-ready*: reading its fields is ok.

* ``L`` is a pointer to a *local* object.  We can always read from
  but not necessarily write to local objects.

* ``W`` is a pointer to a *writable* local object.


``W = Allocate(size)`` allocates a local object::

    def Allocate(size):
        W = malloc(size)
        W->h_global = False
        W->h_possibly_outdated = False
        W->h_written = True
        W->h_version = 0
        return W


``R = LatestGlobalVersion(G)`` takes a pointer ``G`` to a global object,
and if necessary follows the chain of newer versions, until it reaches
the most recent version ``R``.  Then it checks the version number of
``R`` to see that it was not created after ``start_time``.
Pseudo-code::

    def LatestGlobalVersion(G, ...):
        R = G
        while (v := R->h_version) & 1:    # "has a more recent version"
            R = v & ~ 1
        if v > start_time:                # object too recent?
            ValidateFast()                # try to move start_time forward
            return LatestGlobalVersion(G) # restart searching from G
        PossiblyUpdateChain(G, R, ...)    # see below
        return R


``R = DirectReadBarrier(P)`` is the first version of the read barrier.
It takes a random pointer ``P`` and returns a possibly different pointer
``R`` out of which we can read from the object.  The result ``R``
remains valid for read access until either the current transaction ends,
or until a write into the same object is done.  Pseudo-code::

    def DirectReadBarrier(P, ...):
        if not P->h_global:                    # fast-path
            return P
        if not P->h_possibly_outdated:
            R = P
        else:
            R = LatestGlobalVersion(P, ...)
            if R->h_possibly_outdated and R in global_to_local:
                L = ReadGlobalToLocal(R, ...)  # see below
                return L
        R = AddInReadSet(R)                    # see below
        return R


A simple optimization is possible.  If ``R`` is returned by a previous
call to ``DirectReadBarrier`` and the current transaction is still
running, but we could have written to ``R`` in the meantime, then we
need to repeat only part of the logic, because we don't need
``AddInReadSet`` again.  It gives this::

    def RepeatReadBarrier(R, ...):
        if not R->h_possibly_outdated:       # fast-path
            return R
        # LatestGlobalVersion(R) would either return R or abort
        # the whole transaction, so omitting it is not wrong
        if R in global_to_local:
            L = ReadGlobalToLocal(R, ...)    # see below
            return L
        return R


``L = Localize(R)`` is an operation that takes a read-ready pointer to a
global object and returns a corresponding pointer to a local object::

    def Localize(R):
        if R in global_to_local:
            return global_to_local[R]
        L = malloc(sizeof R)
        L->h_global = False
        L->h_possibly_outdated = False
        L->h_written = False
        L->h_version = R          # back-reference to the original
        L->objectbody... = R->objectbody...
        global_to_local[R] = L
        return L


``W = WriteBarrier(P)`` and ``W = WriteBarrierFromReadReady(R)`` are
two versions of the write barrier::

    def WriteBarrier(P):
        if not P->h_global:       # fast-path
            return P
        if P->h_possibly_outdated:
            R = LatestGlobalVersion(P)
        else:
            R = P
        W = Localize(R)
        W->h_written = True
        R->h_possibly_outdated = True
        return W

    def WriteBarrierFromReadReady(P):
        if not R->h_global:       # fast-path
            return R
        W = Localize(R)
        W->h_written = True
        R->h_possibly_outdated = True
        return W


Auto-localization of some objects
----------------------------------------

The "fast-path" markers above are quick checks that are supposed to be
inlined in the caller, so that we only have to pay for a full call to a
barrier implementation when the fast-path fails.

However, even the fast-path of ``DirectReadBarrier`` fails repeatedly
when the ``DirectReadBarrier`` is invoked repeatedly on the same set of
global objects.  This occurs in example of code that repeatedly
traverses the same data structure, visiting the same objects over and
over again.

If the objects that make up the data structure were local, then we would
completely avoid triggering the read barrier's implementation.  So
occasionally, it is better to *localize* global objects even when they
are only read from.

The idea of localization is to break the strict rule that, as long as we
don't write anything, we can only find more global objects starting from
a global object.  This is relaxed here by occasionally making a local
copy even though we don't write to the object.

This is done by tweaking ``AddInReadSet``, whose main purpose is to
record the read object in a set (actually a list)::

    def AddInReadSet(R):
        if R not in recent_reads_cache:
            list_of_read_objects.append(R)
            recent_reads_cache[R] = 1
            # the cache is fixed-size, so the line above
            # possibly evinces another older entry
            return R
        else:
            count = recent_reads_cache[R]
            count += 1
            recent_reads_cache[R] = count
            if count < THRESHOLD:
                return R
            else:
                L = Localize(R) 
                return L


Note that the localized objects are just copies of the global objects.
So all the pointers they normally contain are pointers to further global
objects.  If we have a data structure involving a number of objects,
when traversing it we are going to fetch global pointers out of
localized objects, and we still need read barriers to go from the global
objects to the next local objects.

To get the most out of the optimization above, we also need to "fix"
local objects to change their pointers to go directly to further
local objects.

So ``L = ReadGlobalToLocal(R, R_Container, FieldName)`` is called with
optionally ``R_Container`` and ``FieldName`` referencing some
container's field out of which ``R`` was read::

    def ReadGlobalToLocal(R, R_Container, FieldName):
        L = global_to_local[R]
        if not R_Container->h_global:
            L_Container = R_Container
            L_Container->FieldName = L     # fix in-place
        return L


Finally, a similar optimization can be applied in
``LatestGlobalVersion``.  After it follows the chain of global versions,
it can "compress" that chain in case it contained several hops, and also
update the original container's field to point directly to the latest
version::

    def PossiblyUpdateChain(G, R, R_Container, FieldName):
        if R != G:
            # compress the chain
            while G->h_version != R | 1:
                G_next = G->h_version & ~ 1
                G->h_version = R | 1
                G = G_next
            # update the original field
            R_Container->FieldName = R

