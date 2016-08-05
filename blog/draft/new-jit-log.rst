PyPy Tooling Upgrade: JitViewer and VMProf
=======

We are happy to announce a major JitViewer (JV) update.
JV allows you to inspect PyPy's internal compiler representation including the generated machine code of your program.
A useful tool to spot issues in your program and learn PyPy's compiler details.

VMProf is a statistical cpu profiler imposing very little overhead at runtime.

Both VMProf and JitViewer share a common goal: Present useful information for your Python program. 
The combination of both might reveal more information. That is the reason why they are now both packaged together.
www.vmprof.com also got updated with various bugfixes and changes including an all new interface to JV.

An advertisment: We constantly improve tooling and libraries around the Python/PyPy eco system.
Here are a four examples you might also want to use in your Python projects:

* VMProf - A statistical CPU profiler (http://vmprof.readthedocs.io/en/latest/)
* RevDB - A reverse debugger for Python (https://morepypy.blogspot.co.at/2016/07/reverse-debugging-for-python.html)
* CFFI - Foreign Function Interface that avoids CPyExt (http://cffi.readthedocs.io/en/latest/)
* JitViewer - Visualization of the log file produced by PyPy (http://vmprof.readthedocs.io/en/latest/)

A "brand new" JitViewer
---------------------

The old logging format was a hard to maintain plain text logging facility. Frequent changes often broke internal tools. Additionaly the logging output of a long running program took a lot of disk space.

Our new binary format encodes data densly, makes use of some compression (gzip) and tries to remove repetition where possible. On top of that it supports versioning and can be extended easily. And *drumroll* you do not need to install JV yourself anymore! The whole system moved to vmprof.com and you can use it any time.

Sounds great. But what can you do with it? Here are two examples useful for a PyPy user:

PyPy crashed? Did you discover a bug?
-------------------

For some hard to find bugs it is often necessary to look at the compiled code. The old procedure often required to upload a plain text file which was hard to parse and to look through. 

A new way to share a crash report is to install the ``vmprof`` module from PyPi and execute either of the two commands:

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

Providing the link in the bug report enables PyPy developers browse and identify potential issues.

Speed issues
------------

VMProf is a great tool to find out hot spots that consume a lot of time in your program. As soon as you have idenified code that runs slow, you can switch to jitlog and maybe pin point certain aspects that do not behave as expected. You will find not only the overview, but are also able to browse the generated code. If you cannot make sense of that all you can just share the link with us and we can have a look at too.

Future direction
----------------

We hope that the new release will help both PyPy developers and PyPy users resolve potential issues and easily point them out.

Here are a few ideas what might come in the next few releases:

* Combination of CPU profiles and the JITLOG (Sadly did not make it into the current release)

* Extend vmprof.com to be able to query vmprof/jitlog. An example query for vmprof: 'methods.callsites() > 5' and for the jitlog would be 'traces.contains('call_assembler').hasbridge('*my_func_name*')'.

* Extend the jitlog to capture the information of the optimization stage

Richard Plangger (plan_rich) and the PyPy team

