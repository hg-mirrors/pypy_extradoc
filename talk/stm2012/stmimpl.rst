========================
STM implementation model
========================


Overview
============================================================

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



The STM implementation
============================================================


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
- is_inevitable
- global_to_local
- list_of_read_objects
- recent_reads_cache
- my_lock

The ``start_time`` is the "time" at which the transaction started.  All
reads and writes done so far in the transaction appear consistent with
the state at time ``start_time``.  The global "time" is a single global
number that is atomically incremented whenever a transaction commits.

``is_inevitable`` is a flag described later.

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
            if V >= LOCKED:                # object actually locked?
                goto retry                 # spin-loop to start of func
            ValidateDuringTransaction()    # try to move start_time forward
            goto retry                     # restart searching from R
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
*global* object and returns a corresponding pointer to a local object::

    def Localize(R):
        assert R->h_global
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

    def LocalizeReadReady(R):
        if R->h_global:
            L = Localize(R)
        else:
            L = R
        return L


``W = WriteBarrier(P)`` and ``W = WriteBarrierFromReadReady(R)`` are
two versions of the write barrier::

    def WriteBarrier(P):
        if P->h_written:          # fast-path
            return P
        if not P->h_global:
            W = P
            R = W->h_revision
        else:
            if P->h_possibly_outdated:
                R = LatestGlobalRevision(P)
            else:
                R = P
            W = Localize(R)
        W->h_written = True
        R->h_possibly_outdated = True
        return W

    def WriteBarrierFromReadReady(R):
        if R->h_written:          # fast-path
            return R
        if not R->h_global:
            W = R
            R = W->h_revision
        else:
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
        if R != G and Rarely():
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

``Rarely`` uses a thread-local counter to return True only rarely.  We
do the above update only rarely, rather than always, although it would
naively seem that doing the update always is a good idea.  The problem
is that it generates a lot of write traffic to global data that is
potentially shared between CPUs.  We will need more measurements, but it
seems that doing it too often causes CPUs to stall.  It is probable that
updates done by one CPU are sent to other CPUs at high cost, even though
these updates are not so important in this particular case (i.e. the
program would work fine if the other CPUs didn't see such updates at all
and instead repeated the same update logic locally).


Validation
------------------------------------

``ValidateDuringTransaction`` is called during a transaction to update
``start_time``.  It makes sure that none of the read objects have been
modified since ``start_time``.  If one of these objects is modified by
another commit in parallel, then we want this transaction to eventually
fail.  More precisely, it will fail the next time one of the
``ValidateDuring*`` functions is called.

Note a subtle point: if an object is currently locked, we have to wait
until it gets unlocked, because it might turn out to point to a more
recent version that is still older than the current global time.

Here is ``ValidateDuringTransaction``::

    def ValidateDuringTransaction():
        start_time = GetGlobalCurTime() # copy from the global time
        for R in list_of_read_objects:
            v = R->h_revision
            if not (v & 1):             # "is a pointer", i.e.
                AbortTransaction()      #   "has a more recent revision"
            if v >= LOCKED:             # locked
                spin loop retry         # jump back to the "v = ..." line

The last detection for inconsistency is during commit, when
``ValidateDuringCommit`` is called.  It is a slightly more complex
version than ``ValidateDuringTransaction`` because it has to handle
"locks" correctly.  It also returns a True/False result instead of
aborting::

    def ValidateDuringCommit():
        for R in list_of_read_objects:
            v = R->h_revision
            if not (v & 1):            # "is a pointer", i.e.
                return False           #   "has a more recent revision"
            if v >= LOCKED:            # locked
                if v != my_lock:       # and not by me
                    return False
        return True


Local garbage collection
------------------------------------

Before we can commit, we need the system to perform a "local garbage
collection" step.  The problem is that recent objects (obtained with
``Allocate`` during the transaction) must originally have the
``h_global`` flag set to False, but this must be changed to True before
the commit is complete.  While we could make a chained list of all such
objects and change all their ``h_global`` flags now, such an operation
is wasteful: at least in PyPy, the vast majority of such objects are
already garbage.

Instead, we describe here the garbage collection mechanism used in PyPy
(with its STM-specific tweaks).  All newly allocated objects during a
transaction are obtained from a thread-specific "nursery".  The nursery
is empty when the transaction starts.  If the nursery fills up during
the execution of the transaction, a "minor collection" cycle moves the
surviving objects outside.  All these objects, both from the nursery and
those moved outside, have the ``h_global`` flag set to False.

At the end of the transaction, we perform a "local collection" cycle.
The main goal is to make surviving objects non-movable --- they cannot
live in any thread-local nursery as soon as they are visible from other
threads.  If they did, we could no longer clear the content of the
nursery when it fills up later.

The secondary goal of the local collection is to change the header flags
of all surviving objects: their ``h_global`` is set to True.  As an
optimization, during this step, all pointers that reference a *local but
not written to* object are changed to point directly to the original
global object.

Actual committing occurs after the local collection cycle is complete,
when *all* reachable objects are ``h_global``.

Hand-wavy pseudo-code::

    def FinishTransaction():
        FindRootsForLocalCollect()
        PerformLocalCollect()
        CommitTransaction()          # see below

    def FindRootsForLocalCollect():
        for (R, L) in global_to_local:
            if not L->h_written:     # non-written local objs are dropped
                L->h_global = True   # (becoming global and outdated -> R)
                L->h_possibly_outdated = True
                #L->h_revision is already R
                continue
            gcroots.add(R, L, 0)       # add 'L' as a root

    def PerformLocalCollect():
        collect from the roots...
        for all reached local object,
            change h_global False->True
            and h_written True->False

Note that non-written local objects are just shadow copies of existing
global objects.  For the sequel we just replace them with the original
global objects again.  This is done by tweaking the local objects'
header.


Committing
------------------------------------

Committing is a four-steps process:

1. We first take all global objects with a local copy that has been
written to, and mark them "locked" by putting in their ``h_revision``
field a special value that will cause parallel CPUs to spin loop in
``LatestGlobalRevision``.

2. We atomically increase the global time (with LOCK CMPXCHG).

3. We check again that all read objects are still up-to-date, i.e. have
not been replaced by a revision more recent than ``start_time``.  (This
is the last chance to abort a conflicting transaction; if we do, we have
to remember to release the locks.)

4. Finally, we unlock the global objects by overriding their
``h_revision``.  We put there now a pointer to the corresponding
previously-local object, and the previously-local object's header is
fixed so that it plays from now on the role of the global head of the
chained list.

In pseudo-code::

    def CommitTransaction():
        # (see below for the full version with inevitable transactions)
        AcquireLocks()
        cur_time = global_cur_time
        while not CMPXCHG(&global_cur_time, cur_time, cur_time + 2):
            cur_time = global_cur_time    # try again
        if cur_time != start_time:
            if not ValidateDuringCommit():   # only call it if needed
                AbortTransaction()           # last abort point
        UpdateChainHeads(cur_time)

Note the general style of usage of CMPXCHG: we first read normally the
current version of some data (here ``global_cur_time``), and then do the
expensive CMPXCHG operation.  It checks atomically if the value of the
data is still equal to the old value; if yes, it replaces it with a new
specified value and returns True; otherwise, it simply returns False.
In the latter case we just loop again.  (A simple case like this could
also be done with XADD, with a locked increment-by-two.)

Here is ``AcquireLocks``, locking the global objects.  Note that
"locking" here only means writing a value >= LOCKED in the
``h_revision`` field; it does not involve OS-specific thread locks::

    def AcquireLocks():
        for (R, L, 0) in gcroots SORTED BY R:
            v = R->h_revision
            if not (v & 1):         # "is a pointer", i.e.
                AbortTransaction()  #   "has a more recent revision"
            if v >= LOCKED:         # already locked by someone else
                spin loop retry     # jump back to the "v = ..." line
            if not CMPXCHG(&R->h_revision, v, my_lock):
                spin loop retry     # jump back to the "v = ..." line
            save v into the third item in gcroots, replacing the 0

We use CMPXCHG to store the lock.  This is required, because we must not
conflict with another CPU that would try to write its own lock in the
same field --- in that case, only one CPU can succeed.

Acquiring multiple locks comes with the question of how to avoid
deadlocks.  In this case, it is prevented by ordering the lock
acquisitions in the numeric order of the R pointers.  This should be
enough to prevent deadlocks even if two threads have several objects in
common in their gcroots.

The lock's value ``my_lock`` is, precisely, a very large odd number, at
least LOCKED (which should be some value like 0xFFFF0000).
Such a value causes ``LatestGlobalRevision`` to spin loop until the
lock is released (i.e.  another value is written in ``h_revision``).


After this, ``CommitTransaction`` increases the global time and then
calls ``ValidateDuringCommit`` defined above.  It may still abort.  In
case ``AbortTransaction`` is called, it must release the locks.  This is
done by writing back the original timestamps in the ``h_revision``
fields::

    def CancelLocks():
        for (R, L, v) in gcroots:
            if v != 0:
                R->h_revision = v
                reset the entry in gcroots to v=0

    def AbortTransaction():
        CancelLocks()
        # call longjmp(), which is the function from C
        # going back to the transaction start
        longjmp()


Finally, in case of a successful commit, ``UpdateChainHeads`` also
releases the locks --- but it does so by writing in ``h_revision`` a
pointer to the previously-local object, thus increasing the length of
the chained list by one::

    def UpdateChainHeads(cur_time):
        new_revision = cur_time + 1     # make an odd number
        for (R, L, v) in gcroots:
            #L->h_global is already True
            #L->h_written is already False
            #L->h_possibly_outdated is already False
            L->h_revision = new_revision
            smp_wmb()
            #R->h_possibly_outdated is already True
            R->h_revision = L

``smp_wmb`` is a "write memory barrier": it means "make sure the
previous writes are sent to the main memory before the succeeding
writes".  On x86 it is just a "compiler fence", preventing the compiler
from doing optimizations that would move the assignment to
``R->h_revision`` earlier.  On non-x86 CPUs, it is actually a real CPU
instruction, needed because the CPU doesn't normally send to main memory
the writes in the original program order.  (In that situation, it could
be more efficiently done by splitting the loop in two: first update all
local objects, then only do one ``smp_wmb``, and then update all the
``R->h_revision`` fields.)

Note that the Linux documentation pushes forward the need to pair
``smp_wmb`` with either ``smp_read_barrier_depends`` or ``smp_rmb``.  In
our case we would need an ``smp_read_barrier_depends`` in
``LatestGlobalRevision``, in the loop.  It was omitted here because this
is always a no-op (i.e. the CPUs always provide this effect for us), not
only on x86 but on all modern CPUs.


Inevitable transactions
------------------------------------

A transaction is "inevitable" when it cannot abort any more.  It occurs
typically when the transaction tries to do I/O or a similar effect that
we cannot roll back.  Such effects are O.K., but they mean that we have
to guarantee the transaction's eventual successful commit.

The main restriction is that there can be only one inevitable
transaction at a time.  Right now the model doesn't allow any other
transaction to start or commit when there is an inevitable transaction;
this restriction could be lifted with additional work.

For now, the hint that the system has currently got an inevitable
transaction running is given by the value stored in ``global_cur_time``:
the largest positive number (equal to the ``INEVITABLE`` constant).

``BecomeInevitable`` is called from the middle of a transaction to
(attempt to) make the current transaction inevitable::

    def BecomeInevitable():
        inevitable_mutex.acquire()
        cur_time = global_cur_time
        while not CMPXCHG(&global_cur_time, cur_time, INEVITABLE):
            cur_time = global_cur_time    # try again
        if start_time != cur_time:
            start_time = cur_time
            if not ValidateDuringCommit():
                global_cur_time = cur_time     # must restore the value
                inevitable_mutex.release()
                AbortTransaction()
        is_inevitable = True

We use a normal OS mutex to allow other threads to really sleep instead
of spin-looping until the inevitable transaction finishes.  So the
function ``GetGlobalCurTime`` is defined to return ``global_cur_time``
after waiting for other inevitable transaction to finish::
    
    def GetGlobalCurTime():
        assert not is_inevitable    # must not be myself inevitable
        t = global_cur_time
        if t == INEVITABLE:         # there is another inevitable tr.?
            inevitable_mutex.acquire()   # wait
            inevitable_mutex.release()
            return GetGlobalCurTime()    # retry
        return t

Then we extend ``CommitTransaction`` for inevitable support::

    def CommitTransaction():
        AcquireLocks()
        if is_inevitable:
            cur_time = start_time
            if not CMPXCHG(&global_cur_time, INEVITABLE, cur_time + 2):
                unreachable: no other thread changed global_cur_time
            inevitable_mutex.release()
        else:
            cur_time = GetGlobalCurTimeInCommit()
            while not CMPXCHG(&global_cur_time, cur_time, cur_time + 2):
                cur_time = GetGlobalCurTimeInCommit()  # try again
            if cur_time != start_time:
                if not ValidateDuringCommit():   # only call it if needed
                    AbortTransaction()           # last abort point
        UpdateChainHeads(cur_time)

    def GetGlobalCurTimeInCommit():
        t = global_cur_time
        if t == INEVITABLE:
            CancelLocks()
            inevitable_mutex.acquire()   # wait until released
            inevitable_mutex.release()
            AcquireLocks()
            return GetGlobalCurTimeInCommit()
        return t



Barrier placement in the source code
============================================================


Overview
-----------

Placing the read/write barriers in the source code is not necessarily
straightforward, because there are a lot of object states to choose
from.  The barriers described above are just the most common cases.

We classify here the object categories more precisely.  A pointer to an
object in the category ``R`` might actually point to one that is in the
more precise category ``L`` or ``W``.  Conversely, a pointer to an
object in the category ``L`` is also always in the categories ``R`` or
``O``.  This can be seen more generally in the implication
relationships::

     W => L => R => O => P       G => P    (I)

A letter X is called *more general than* a letter Y if ``Y => X``, and
*more precise than* a letter Y if ``X => Y``.

Barriers are used to make an object's category more precise.  Here are
all 12 interesting conversions, with the five functions from the section
`Read/write barriers design`_ (abbreviated as DRB, RRB, LRR, WrB and
WFR) as well as seven more potential conversions (written ``*``) that
could be implemented efficiently with slight variations:

    +--------+-----------------------------------+
    |        |                From               |
    +--------+-----+-----+-----+-----+-----+-----+
    |   To   |  P  |  G  |  O  |  R  |  L  |  W  |
    +========+=====+=====+=====+=====+=====+=====+
    |     R  | DRB |``*``| RRB |                 |
    +--------+-----+-----+-----+-----+-----------+
    |     L  |``*``|``*``|``*``| LRR |           |
    +--------+-----+-----+-----+-----+-----+-----+
    |     W  | WrB |``*``|``*``| WFR |``*``|     |
    +--------+-----+-----+-----+-----+-----+-----+

In the sequel we will refer to each of the 12 variations as *X2Y*
for X in ``P, G, O, R, L`` and Y in ``R, L, W``.


Constraints
-----------

The source code's pointer variables are each assigned one letter
from ``P, G, O, R, L, W`` such that:

* A variable is only passed into another variable with either the same
  or a more general letter.  This holds for intra- as well as
  inter-procedural definitions of "being passed" (i.e. also for
  arguments and return value).

* Read/write barriers can be inserted at any point, returning a variable
  of a more precise letter.

* Any read must be done on an object in category ``R, L, W``.  Any write
  must be done on an object in category ``W``.  Moreover an object must
  only be in category ``W`` if we can prove that a write necessarily
  occurs on the object.

* The ``L2W`` barrier is very cheap.  It is also the only barrier which
  doesn't need to return a potentially different pointer.  However,
  converting objects to the ``L`` category in first place (rather than
  ``R``) has a cost.  It should be done only for the objects on which we
  are *likely* to perform a write.

* An object in the ``R`` category falls back automatically to the ``O``
  category if we perform an operation (like a call to an unrelated
  function) that might potentially cause it to be written to.

* If we do a call that might cause the current transaction to end and
  the next one to start, then all live variables fall back to the ``P``
  category.

* The ``G`` category is only used by prebuilt constants.  In all
  other cases we don't know that a pointer is definitely not a local
  pointer.  The ``NULL`` constant is in all categories; ``G`` and ``L``
  have only ``NULL`` in common.

* In general, it is useful to minimize the number of executed barriers,
  and have the cheapest barriers possible.  If, for example, we have a
  control flow graph with two paths that reach (unconditionally) the
  same write location, but on one path the object is a ``R`` (because we
  just read something out of it) and on the other path the object is a
  ``G`` (because it is a global on which we did not perform any read),
  then we should insert the ``R2W`` barrier at the end of the first path
  and the ``G2W`` barrier at the end of the second path, rather than the
  ``P2W`` barrier only once after the control flow merges.

Pseudo-code for some of the remaining barriers::

    def G2R(G):
        assert G->h_global
        return P2R(G)        # the fast-path never works

    def G2W(G):
        assert G->h_global
        assert not G->h_written
        if G->h_possibly_outdated:
            R = LatestGlobalRevision(G)
        else:
            R = G
        W = Localize(R)
        W->h_written = True
        R->h_possibly_outdated = True
        return W

    def L2W(L):
        if L->h_written:    # fast-path
            return L
        L->h_written = True
        L->h_revision->h_possibly_outdated = True
        return L

