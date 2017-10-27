PyPy Tooling Upgrade: JitViewer and VMProf
=======

We are happy to announce a major JitViewer (JV) update.
JV allows you to inspect RPython's internal compiler representation (the language in which PyPy is implemented)
including the generated machine code of your program.
It can graphically show you details of the RPython compiled code and helps you pinpoint issues in your code.

VMProf is a statistical CPU profiler for python imposing very little overhead at runtime.

Both VMProf and JitViewer share a common goal: Present useful information for your python program. 
The combination of both can reveal more information than either alone. 
That is the reason why they are now both packaged together.
We also updated www.vmprof.com with various bug fixes and changes including an all new interface to JV.

This work was done with the goal of improving tooling and libraries around the Python/PyPy/RPython ecosystem.
Some of the tools we have developed:

* CFFI - Foreign Function Interface that avoids CPyExt (http://cffi.readthedocs.io/en/latest/)
* RevDB - A reverse debugger for python (https://morepypy.blogspot.co.at/2016/07/reverse-debugging-for-python.html)

and of course the tools we discuss here:

* VMProf - A statistical CPU profiler (http://vmprof.readthedocs.io/en/latest/)
* JitViewer - Visualization of the log file produced by RPython (http://vmprof.readthedocs.io/en/latest/)

A "brand new" JitViewer
---------------------

JitViewer has two pieces: you create a log file when running your program, and then use a graphic tool to view what happened.

The old logging format was a hard-to-maintain, plain-text-logging facility. Frequent changes often broke internal tools. 
Additionally, the logging output of a long running program required a lot of disk space.

Our new binary format encodes data densely, makes use of some compression (gzip), and tries to remove repetition where possible. 
It also supports versioning for future proofing and can be extended easily. 

And *drumroll* you no longer need to install a tool to view the log yourself
anymore! The whole system moved to vmprof.com and you can use it any time.

Sounds great. But what can you do with it? Here are two examples for a PyPy user:

PyPy crashed? Did you discover a bug?
-------------------

For some hard to find bugs it is often necessary to look at the compiled code. The old
procedure often required you to upload a plain text file which was hard to parse and to look through. 

A better way to share a crash report is to install the ``vmprof`` module from PyPi and execute either of the two commands:

```
# this program does not crash, but has some weird behaviour
$ pypy -m jitlog --web <your program args>
...
PyPy Jitlog: http://vmprof.com/#/<hash>/traces
# this program segfaults
$ pypy -m jitlog -o /tmp/log <your program args>
...
<Segfault>
$ pypy -m jitlog --upload /tmp/log
PyPy Jitlog: http://vmprof.com/#/<hash>/traces
```

Providing the link in the bug report allows PyPy developers to browse and identify potential issues.

Speed issues
------------

VMProf is a great tool to find hot spots that consume a lot of time in your program. As soon as you have identified code that runs slowly, you can switch to jitlog and maybe pinpoint certain aspects that do not behave as expected. You will find an overview, and are able to browse the generated code. If you cannot make sense of all that, you can just share the link with us and we can have a look too.

Future direction
----------------

We hope that the new release will help both PyPy developers and PyPy users resolve potential issues and easily point them out.

Here are a few ideas what might come in the next few releases:

* Combination of CPU profiles and the JITLOG (sadly did not make it into the current release).

* Extend vmprof.com to be able to query vmprof/jitlog. An example query for vmprof: 'methods.callsites() > 5' and for the jitlog would be 'traces.contains('call_assembler').hasbridge('*my_func_name*')'.

* Extend the jitlog to capture the information of the optimization stage.

Richard Plangger (plan_rich) and the PyPy team

