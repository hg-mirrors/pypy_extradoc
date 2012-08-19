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
of global revisions.

It is the job of the GC to collect the older revisions when they are
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

Every object has a header with these fields:

- h_global (boolean)
- h_possibly_outdated (boolean)
- h_written (boolean)
- h_revision (unsigned integer)

The h_revision is an unsigned "revision number" that can also
alternatively contain a pointer.  The other fields are flags.  (In
practice they are just bits inside the GC h_tid field.)

- ``h_global`` means that the object is a global object.

- ``h_possibly_outdated`` is used as an optimization: it means that the
  object is possibly outdated.  It is False for all local objects.  It
  is also False if the object is a global object, is the most recent of
  its chained list of revisions, and is known to have no modified local
  version in any transaction.

- ``h_written`` is set on local objects that have been written to.

- ``h_revision`` on local objects points to the global object that they
  come from, if any; otherwise it is 1.

- ``h_revision`` on global objects depends on whether the object is the
  head of the chained list of revisions or not.  If it is, then
  ``h_revision`` contains the "timestamp" of the revision at which this
  version of the object was committed.  This is an odd number.  For
  non-head revisions, ``h_revision`` is a pointer to a more recent
  revision.  A pointer is always an even number.


Transaction details
-------------------

Every CPU is either running one transaction, or is busy trying to commit
the transaction it has so far.  The following data is transaction-local:

- start_time
- global_to_local
- list_of_read_objects
- recent_reads_cache
- my_lock

The ``start_time`` is the "time" at which the transaction started.  All
reads and writes done so far in the transaction appear consistent with
the state at time ``start_time``.  The global "time" is a single global
number that is atomically incremented whenever a transaction commits.

``global_to_local`` is a dictionary-like mapping of global objects to
their corresponding local objects.

``list_of_read_objects`` is a set of all global objects read from, in
the revision that was used for reading.  It is actually implemented as a
list, but the order or repetition of elements in the list is irrelevant.

``recent_reads_cache`` is a fixed-size cache that remembers recent
additions to the preceeding list, in order to avoid inserting too much
repeated entries into the list, as well as keep lightweight statistics.

``my_lock`` is a constant in each thread: it is a very large (>= LOCKED)
odd number that identifies the thread in which the transaction runs.


Read/write barriers design
---------------------------------------

The read/write barriers are designed with the following goals in mind:

- In the source code (graphs from RPython), variables containing
  pointers can be annotated as beloning to one of 6 categories:

  * ``P`` is a pointer to any object.

  * ``G`` is a pointer to a *global* object.

  * ``R`` is a pointer to an object that was checked for being
    *read-ready*: reading its fields is ok.

  * ``O`` is an *old* pointer that used to be read-ready, but in which
    we may have written to in the meantime

  * ``L`` is a pointer to a *local* object.  We can always read from
    but not necessarily write to local objects.

  * ``W`` is a pointer to a *writable* local object.

- The goal is to insert calls to the following write barriers so that we
  only ever read from objects in the ``R``, ``L`` or ``W`` categories,
  and only ever write to objects in the ``W`` category.

- Global objects are immutable, and so can only contain pointers to
  further global objects.

- The read barriers themselves need to ensure that
  ``list_of_read_objects`` contains exactly the set of global objects
  that have been read from.  These objects must all be of the most
  recent revision that is not more recent than ``start_time``.  If an
  object has got a revision more recent than ``start_time``, then the
  current transaction is in conflict.  The transaction is aborted as
  soon as this case is detected.

- The write barriers make sure that all modified objects are local and
  the ``h_written`` flag is set.

- All barriers ensure that ``global_to_local`` satisfies the following
  property for any local object ``L``: either ``L`` was created by
  this transaction (``L->h_revision == 1``) or else satisfies
  ``global_to_local[L->h_revision] == L``.


Pseudo-code for read/write barriers
---------------------------------------

``W = Allocate(size)`` allocates a local object::

    def Allocate(size):
        W = malloc(size)
        W->h_global = False
        W->h_possibly_outdated = False
        W->h_written = True
        W->h_revision = 1
        return W


``R = LatestGlobalRevision(G)`` takes a pointer ``G`` to a global object,
and if necessary follows the chain of newer revisions, until it reaches
the most recent revision ``R``.  Then it checks the revision number of
``R`` to see that it was not created after ``start_time``.
Pseudo-code::

    def LatestGlobalRevision(G, ...):
        R = G
        while not (v := R->h_revision) & 1:# "is a pointer", i.e.
            R = v                          #   "has a more recent revision"
        if v > start_time:                 # object too recent?
            ValidateDuringTransaction()    # try to move start_time forward
            return LatestGlobalRevision(R) # restart searching from R
        PossiblyUpdateChain(G, R, ...)     # see below
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
            R = LatestGlobalRevision(P, ...)
            if R->h_possibly_outdated and R in global_to_local:
                L = ReadGlobalToLocal(R, ...)  # see below
                return L
        R = AddInReadSet(R)                    # see below
        return R


A simple optimization is possible.  Assume that ``O`` is a pointer
returned by a previous call to ``DirectReadBarrier`` and the current
transaction is still running, but we could have written to ``O`` in the
meantime.  Then we need to repeat only part of the logic, because we
don't need ``AddInReadSet`` again.  It gives this::

    def RepeatReadBarrier(O, ...):
        if not O->h_possibly_outdated:       # fast-path
            return O
        # LatestGlobalRevision(O) would either return O or abort
        # the whole transaction, so omitting it is not wrong
        if O in global_to_local:
            L = ReadGlobalToLocal(O, ...)    # see below
            return L
        R = O
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
        L->h_revision = R          # back-reference to the original
        L->objectbody... = R->objectbody...
        global_to_local[R] = L
        return L


``W = WriteBarrier(P)`` and ``W = WriteBarrierFromReadReady(R)`` are
two versions of the write barrier::

    def WriteBarrier(P):
        if not P->h_global:       # fast-path
            return P
        if P->h_possibly_outdated:
            R = LatestGlobalRevision(P)
        else:
            R = P
        W = Localize(R)
        W->h_written = True
        R->h_possibly_outdated = True
        return W

    def WriteBarrierFromReadReady(R):
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
``LatestGlobalRevision``.  After it follows the chain of global
revisions, it can "compress" that chain in case it contained several
hops, and also update the original container's field to point directly
to the latest version::

    def PossiblyUpdateChain(G, R, R_Container, FieldName):
        if R != G:
            # compress the chain
            while G->h_revision != R:
                G_next = G->h_revision
                G->h_revision = R
                G = G_next
            # update the original field
            R_Container->FieldName = R

This last line is a violation of the rule that global objects are
immutable.  It still works because it is only an optimization that will
avoid some chain-walking in the future.  If two threads conflict in
updating the same field to possibly different values, it is undefined
what exactly occurs: other CPUs can see either the original or any of
the modified values.  It works because the original and each modified
value are all interchangeable as far as correctness goes.


Validation
------------------------------------

``ValidateDuringTransaction`` is called during a transaction to update
``start_time``.  It makes sure that none of the read objects have been
modified since ``start_time``::

    def ValidateDuringTransaction():
        start_time = global_cur_time    # copy from the global time
        for R in list_of_read_objects:
            if not (R->h_revision & 1): # "is a pointer", i.e.
                AbortTransaction()      #   "has a more recent revision"

If such an object is modified by another commit, then this transaction
will eventually fail --- hopefully, the next time
``ValidateDuringTransaction`` is called.

The last detection for inconsistency is during commit, when
``ValidateDuringCommit`` is called.  It is a slightly more complex
version than ``ValidateDuringTransaction`` because it has to handle
"locks" correctly::

    def ValidateDuringCommit():
        for R in list_of_read_objects:
            v = R->h_revision
            if not (v & 1):            # "is a pointer", i.e.
                AbortTransaction()     #   "has a more recent revision"
            if v >= LOCKED:            # locked
                if v != my_lock:       # and not by me
                    spin loop retry    # jump back to the "v = ..." line


Committing
------------------------------------

Committing is a four-steps process:

1. We first find all global objects that we have written to, and mark
them "locked" by putting in their ``h_revision`` field a special value
that will cause parallel CPUs to spin loop in ``LatestGlobalRevision``.
We also prepare the local versions of these objects to become the next
head of the chained lists, by fixing the headers.

2. We atomically increase the global time (with LOCK CMPXCHG).  This
causes a MFENCE too: all prepared local objects are visible to all other
CPUs afterwards.

3. We check again that all read objects are still up-to-date, i.e. have
not been replaced by a revision more recent than ``start_time``.  (This
is the last chance to abort a conflicting transaction; if we do, we have
to remember to release the locks.)

4. Finally, we unlock the global objects by overriding their
``h_revision``.  We put there now a pointer to the corresponding
previously-local object.  The previously-local object plays from now on
the role of the global head of the chained list.

In pseudo-code::

    def CommitTransaction():
        cur_time = global_cur_time
        AcquireLocks(cur_time)
        while not CMPXCHG(&global_cur_time, cur_time, cur_time + 2):
            cur_time = global_cur_time    # try again
            AcquireLocksAgain(cur_time)
        ValidateDuringCommit()
        UpdateChainHeads()

Note the general style of usage of CMPXCHG: we first read normally the
current version of some data (here ``global_cur_time``), do some
preparations based on this value (here ``AcquireLocks``), and then do
the expensive CMPXCHG operation.  It checks atomically if the value 
of the data is still equal to the old value; if yes, it replaces it
with a new specified value and returns True; otherwise, it simply
returns False.  In the latter case we just loop again.

Here is ``AcquireLocks``, doing both the locking of the global objects
and the fixing of the local objects.  This is done together *before* we
use CMPXCHG, so that after a successful CMPXCHG the other CPUs are
guaranteed to see the new values --- both the locks and the
previously-local objects with the proper fixes.

Note that "locking" here only means writing a value >= LOCKED in the
``h_revision`` field; it does not involve OS-specific thread locks::

    def AcquireLocks(cur_time):
        new_revision = cur_time + 1     # make an odd number
        for (R, L) in global_to_local:
            L->h_global = True
            if not L->h_written:
                #L->h_revision already points to R
                L->h_possibly_outdated = True
                continue
            L->h_revision = new_revision
            L->h_written = False
            #L->h_possibly_outdated is already False
            v = R->h_revision
            if not (v & 1):         # "is a pointer", i.e.
                AbortTransaction()  #   "has a more recent revision"
            if v >= LOCKED:         # already locked by someone else
                spin loop retry     # jump back to the "v = ..." line
            if not CMPXCHG(&R->h_revision, v, my_lock):
                spin loop retry     # jump back to the "v = ..." line
            locks_acquired.add(R, L, v)

(Note that for non-written local objects, we skip this locking entirely;
instead, we turn the object into a "global but outdated" object, keeping
the same ``h_revision`` but with a different meaning.)

We use CMPXCHG to store the lock.  This is required, because we must
not conflict with another CPU that would try to write the same lock
in the same field --- in that case, only one CPU can succeed.

The lock's value ``my_lock`` is, precisely, a very large odd number, at
least LOCKED (which should be some value like 0xFFFF0000).  As we can
check, this is enough to cause ``LatestGlobalRevision`` to spin loop,
calling ``ValidateDuringTransaction`` over and over again, until the
lock is released (i.e.  another value is written in ``h_revision``).

``AcquireLocksAgain`` is called instead of ``AcquireLocks`` if the first
CMPXCHG fails in ``CommitTransaction``.  It just needs to update the
previously-local object's ``h_revision``, keeping the already-acquired
locks::

    def AcquireLocksAgain(cur_time):
        new_revision = cur_time + 1
        for (R, L, v) in locks_acquired:
            L->h_revision = new_revision


In case ``AbortTransaction`` is called, it must release the locks.  This
is done by writing back the original timestamps in the ``h_revision``
fields::

    def AbortTransaction():
        for R, L, v in locks_acquired:
            R->h_revision = v
        # call longjmp(), which is the function from C
        # going back to the transaction start
        longjmp()


Finally, in case of a successful commit, ``UpdateChainHeads`` also
releases the locks --- but it does so by writing in ``h_revision`` a
pointer to the previously-local object, thus increasing the length of
the chained list by one::

    def UpdateChainHeads():
        for (R, L, v) in locks_acquired:
            R->h_version = L
