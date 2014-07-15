------------------------------------------------------------------------------
Using All These Cores: Transactional Memory in PyPy
------------------------------------------------------------------------------


===========================================
Part 1 - Intro and Current Status
===========================================

- stm/demo/

- stm/bottle/

- transaction module; multiprocessing-like Pool(); etc.

- a large demo of some well-known program where
  it solves everything?... there is no such thing
  because the large program's author have already
  solved it

- compare with garbage collection in C:

  - usually you do it with malloc()/free()

  - sometimes you need more control, and e.g. you add
    some reference counts

  - sometimes you use more specialized versions for
    performance, e.g. allocate in a pool and throw it
    completely away at the end of some phase

  - Boehm GC, a GC for C: what kind of demo can you
    present for it?  You take a C program, remove all
    free(), relink malloc() to Boehm, and it works
    more slowly...

  - nevertheless, GCC did exactly that.  Why?

- so, the GIL: we already have different workarounds for
  different kinds of problems (use "multiprocessing"; or
  start N processes and have them communicate in one
  way or another)

- this talk is about the GIL's equivalent of the Boehm GC
  for C: simplify your life for some problems, with a
  reasonable performance cost

- the problems are:

  - anything where the GIL is a blocker, obviously

  - but also any program with "often-parallelizable"
    sections of code



===========================================
Part 2 - Under The Hood
===========================================


- pictures "GIL" and "no GIL"

- zoom with reads and writes

- keep boundaries, each block is a _transaction_

- completely the same semantics as when run with a GIL

- write-write conflict

- deadlock detection and resolution by abort-retry

- read-write conflict: avoids (1) crashes,
  (2) reads-from-the-past, (3) reads-from-the-future

- reads are more common than writes: optimize read barriers

- pypy-stm: write a thread-local flag "this object has been read",
  show code for read barrier and fast-path of write barrier;
  note about using the C library for CPython too

- reads are not synchronized at all between CPUs, but it's wrong
  to read data written by other in-progress transactions;
  so we have to write elsewhere

- but what if we read later an object we modified?  doing any kind
  of check in the read barrier makes it much more costly

- a solution would be to give each thread its own "segment" of
  memory, and copy data between them only at known points

- mmap trick: we do that, but we use mmap sharing to view the same
  pages of memory at several addresses in memory

- show clang source code and assembler for %gs

- picture with 15/16 objects, 1/16 read markers, one page control data

- picture with nursery -- the GC can use the same write barrier



===========================================
Part 3 - Multithreading Revisited
===========================================


- 
