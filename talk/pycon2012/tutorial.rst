How to get the most out of your PyPy
====================================

Description:

For many applications PyPy can provide performance benefits right out
of the box. However, little details can push your application to
perform much better.  In this tutorial we'll give you insights on how
to push pypy to it's limites. We'll focus on understanding the
performance characteristics of PyPy, and learning the analysis tools
in order to maximize your applications performance. For people new to
PyPy we'll also briefly cover making sure your application runs on
PyPy.

Abstract:

We aim to teach people how to use performance tools available for PyPy
as well as to understand PyPy's performance characteristics. We'll explain
how different parts of PyPy interact (JIT, the garbage collector, the virtual
machine runtime) and how to measure which part is eating your time. We'll give
you a tour with jitviewer which is a crucial tool for understanding how your
Python got compiled to assembler and whether it's performing well. We also plan
to show potential pitfalls and usage patterns in the Python language that perform
better or worse in the case of PyPy.

This tutorial is intended for people familiar with Python who have performance
problems, no previous experience with PyPy is needed. We ask people to come
with their own problems and we'll provide some example ones. Attendees should
have the latest version of PyPy preinstalled on their laptops.

Audience level:

Intermediate, people with Python experience but no prior PyPy experiance.
No knowledge of profiling tools is necessary. It is also not needed to know
assembler :)

Additional notes (this goes to reviewers only):

Our intended format is going to be a brief presentation on the architecture of
PyPy, as well as an overview of the tools. From there we'd like to spend the
remainder of the session reviewing practical problems, and showing the steps
to understanding real applications' performance. We'll bring our own example
problems, but we're also going to collect examples from students in advance.

Both presenters have spoken at many previous PyCons, as well as other
conferences, they're also both very active PyPy core developers.

We don't think tutorial assistants would be necessary.

It's a bit hard to give a reasonable outline by now. Since the project
evolves a lot, it's very likely a completely new set of tools will
be available by the time we conduct the tutorial.
