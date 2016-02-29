Tasks
=====

- mercurial benchmarks on PyPy runner exists, some benchmarks
- mercurial porting C extensions to cffi MORE PROGRESS (fijal)
- fix multiple inheritance resolution in cpyext (arigo, cfbolz around)
- py3k work FIXING EVEN MORE TESTS, MERGED DEFAULT (AGAIN) (manuel, ronan)
- register allocator, more information is now available, FIRST PROTOTYPE (remi, richard if remi has time), created an issue
- clean up project lists (ronan, fijal)
- test optimizeopt chain with hypothesis (cfbolz, fijal to discuss)
- try fix speed center (richard, fijal to get him access), created issue
- go skiing (marmoute)
- go shopping
- turn won't manage into issues (all)
- start with new binary jit-log-opt (richard, fijal)
- fixing stm (remi)
- fix buffer API (arigo, fijal)




won't manage
--------------------

- VMProf on OS X, fix bugs (can't reproduce)
- jit leaner frontend
- live ranges in JIT viewer
- fix logging to not take time MESS
- continuing to refactoring annotator
- add warmup time to VMProf
- use probablistic data structures for guard_value, WE HAVE A PLAN
- single-run branch progress
- update setup.py and upload rpython to pip


done:
---------
- dict-proxy with cpyext DONE
- fix bug in FixedSizeArray DONE
- compress resume data more, play with hypothesis (cfbolz, arigo, fijal) DONE
- maps reordering DONE
- take funding calls off the website, write blog post DONE
- fix lxml on cpyext-gc-support-2 (ronan, arigo) DONE, MERGED
- apply vmprof to a non pypy lang (cfbolz, fijal around) DONE
- talk benchmark statistics (cfbolz, mattip, ronan) DONE
- merging default into stm (remi) LESS MESS, MERGING DONE
- cpyext-gc-support-2 blog post (mattip, arigo) DONE
- get data about test duration DONE
- start a bit of a dev process document
- merging cpyext-ext, numpy-on-cpyext NEXT NEXT SEGFAULT, IMPORTS NUMPY WITH ONE HACK
- fix tests
- a script to upload to bitbucket IN PROGRESS
- have a test in rpython that checks against imports from pypy (cfbolz)
- make snowperson (cfbolz, fijal)
- general wizardry (cfbolz, arigo, samuele not around) 


too many bridges
-------------------------

Problems:
 -  pypy py.test is slow
 - most bridges come from guard_value(map) (then guard_class)

Steps:
 - detect the situation (cardinality estimation)
 - trace a general version
 - look at all promotes in pypy, to see whether the general version is good
 - in particular, we need to general version for maps
 - make maps give up if the object is too big

Research:
 - how to deal with method invocations of the same method on different classes
 - 


Python3
=========
  - add more rposix features, use less replacements of os.XXX
  - merge py3.3 -> py3k and create py3.5
  - solve the speed issue
  - utf8 & unicode problems
   - list of things we suspect are slow on pypy3k:
     * unicode & utf8 strings and dictionaries of those strings, potential solution
       is not to use rpython unicode type
     * itertools stuff is slower than python 3
  - manuel & ronan go and work and SFC
  - what to do with crowdfunding


Idea around Mercurial
==================
(notes about "new" feature that could be useful in pypy

- clone bundle,
- share.pool,
- people version,



summer of code
=============

- volunteers from the pypy side: fijal, ronan, richard, remi, backup: armin
- looking for students: richard, remi
- unicode stuff as project



cpyext+numpy
============

- two approaches:
  - micronumpy: basically works, but no story for cpyext, bit of a dead end
  - using numpy code with cpyext, with hooks into micronumpy

- safe (but maybe slow) default, everything just works
- hard part: hijack some of the functionality and replace it with micronumpy code
- ––> Bucharest?



tooling
=======

technical problems:
- too many tools (vmprof, jitviewer, stmlog)
- too many output formats (vmprof, jit-log-opt, stmlog*2)
- jit-log-opt output format is brittle
- parsing debug_merge_point is brittle
- not good fallbacks
- a lot of pypy-specific
- identifying traces is not unique


consolidation goals:
- better format for jit-log-opt (keeping a way to show the old ascii output)
- having a programmatic way to turn on trace dumps
- combining vmprof/jitviewer
- documentation/tutorial

future cool features:
- memory
- warmup time
- extensible events
- web app changes respectively
- navigation in jitviewer
- way to compare runs
- rpython functions where ops are coming from
- threading and forking support


volunteers:
- Maciek
- Matti
- Richard
- Sebastian


steps:
- collect interesting examples
- embed jit-log-opt into vmprof-file
- web stuff

buildbot:
- script/url to start/stop master
- account for matti




unstucking benchmarking
====================

problems:
- py3k what benchmarks are there, where would we run them (and store the results)
- split benchmark running
- comparisons are broken (javascript exception)
- old version with custom hacks that are not backed up??
- access to raw data
- store all the raw data
- benchmarks are too quick on jit / too slow on interp
- non consistent approach to warmup
- we don't have errors
- what to do with historical data
- what to do with branch data

simple steps to improve the situation:
- revive single run branch
- fix comparison (simple if you know JS)
- add an api to get the data
- upload json files to buildbot

harder steps to improve the situation:
- idea: tooling sprint
- move to new machine
- rerun benchmarks
- upgrade benchmarks (particularly the libraries)
- larger bechmarks
- make unreliable benchmarks reliable
- automatic slowdown reporting


volunteer:
- fijal?, cfbolz?, arigo?
- start a bit during the sprint (Thursday)


code quality & failing tests
=====================

problems:
- tests fail for too long
- general instability of recent releases (mostly the fault of unrolling)
- some non-modular impenetrable code:
  - ll2ctypes
  - unroll
  - cpyext
  - structure of the jit optimizing chain
- tests are slow

solutions:
- ll2ctypes: use cffi (see other discussion)
- unroll: reducing features is the only idea we currently have
- on the process level:
  - release candidates
  - RC PPAs?
  - don't merge default into release branch
  - be more principled about bugfix releases
  - do the bugfix also on the latest release branch
  - reduce the overhead of doing bugfix releases:
    - look into automated bitbucket uploading
- use hypothesis more!
- run our own tests on pypy!
- run tests in parallel

Bitbucket related questions
====================
Bitbucket:
- "We are not unhappy with bitbucket; Much better than anything we have before"
- API to upload binary [question asked]
- limited bandwidth to upload
- limited bandwidth to download
- push speed
- clone speed [cloning under a minute on the way]
- email notification "not usable": [improvement planned]
  - a mail per push (not per commit)
  - format → trimmed log message//trimmed diff.
  - "From committer" wanted.
- blocking --force (prevent multiple heads) [on their roadmap]
- Comment on random commit/pull request.

rffi discussion
==========

what do we want in the end:
1) an interface like cffi used at the interpreter level and in rpython/*.
2) rtyping, gctransformer use lltype objects

problems:

- interface & implementation of ll2ctypes
- difference between translated pypy and test env
- deprecated api (rawffi, rawffi_alt)
- no special support for rffi in the annotator?? (seems unclear)

how do we go forward:

- create small examples (e.g. crypt module) that use cffi for testing and at the later point in see
  how we can support full translation.
  rffi.llexternal -> variants that release the gil, some don't. how do we readd the possibility
  of doing the same using cffi?

Example:

sandbox_safe: where do we put the flag so that the annotator understands that?
- preprocess step in cdef
  common agreement to use pragma to define this flags (e.g
    #pragma sandboxmode on -> off

volunteer for the first small module:
maybe scope for gsoc? manuel after merging py3.3


Numpy Hijacking
------------------------

Start over with a different module that uses the multiarray type from numpy instead of W_NDimArray
Make it use indexing for the first step, start copying methods from micronumpy
use raw_virtual


a fast trace hook
------------------------



support virtualenvs natively
---------------------------------------
  * needed to implement venv module on Python 3.3+
  * consider backporting to 2.7 to help virtualenv
  * poke Donal to mail rationale to pypy-dev
  
  
STM
--------

Problems:
 - performance
 - what kind of conflicts are reasonable?
 - how many conflicts are still ok?
 - very slow warmup
 - too many major collections
 - what's the overhead of tiny transactions?
 - need more data!
 - maybe shorter transactions?
 - measure, measure, measure
 - talk to Intel

ideas:
 - find an application that we can speed up
 - write a framework for that
 - try to find a real-world something
