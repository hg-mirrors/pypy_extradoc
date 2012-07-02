=========================================
Performance analysis tools for JITted VMs
=========================================

Who am i
========

* worked on PyPy for 5+ years

* often presented with a task "my program runs slow"

* never completely satisfied with present solutions

|pause|

* I'm not antisocial, just shy (you can talk to me)

What I'll talk about
====================

|pause|

* apologies for a lack of advanced warning - this is a rant

|pause|

* I'll talk about tools

* looking at present solutions

* trying to use them

* what can we do to make situation better

Why a rant?
===========

* making tools is hard

* I don't think any of the existing solutions is as good as it can be

* I'll even rant about my own tools

* JITs don't make it easier

Let's talk about profiling
==========================

* great example - simple twisted application

* there is a builtin module call cProfile, let's use it!

More profiling
===================

* ``lsprofcalltree``

* surely pypy guys should have figured something out...

|pause|

* ``jitviewer``

* some other tools

Let's talk about editors
========================

* vim, emacs

* IDEs

What I really want?
===================

* I want all of it integrated (coverage, tests, profiling, editing)

* with modern interfaces

* with fast keyboard navigation

* with easy learning curve

* with high customizability

Is this possible?
=================

* I don't actually know, but I'll keep trying

Q&A
===

* I'm actually listening for advices
