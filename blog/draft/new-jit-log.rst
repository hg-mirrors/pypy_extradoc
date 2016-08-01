PyPy's Toolbox got a new Hammer &#x1f528;
=======

.. : XXX the title is very generic

.. : XXX I don't actually like the first paragraph, I think it should be more
    to the point. eg that things happened at the Leysin sprint doesn't matter much.
    I would also add links to all the existing tools

Tools, tools, tools! It seems that PyPy cannot get enough of them!
In the last winter sprint (Leysin) covered the current tool for observing internals of the JIT compiler (JitViewer). VMProf at that time already proved that it is a good tool for CPU profiles. We are happy to release a new version of VMProf incorporating a rewritten version of JitViewer.

The old logging format was a hard to maintain plain text logging facility. Frequent changes often broke internal tools, most notably the JITViewer. Another problem was that the logging output of a long running program took a lot of disk space.

Our new binary format encodes data densly, makes use of some compression (gzip) and tries to remove repetition where possible. On top of that protocol supports versioning and can be extended easily. And *drumroll* you do not need to install JitViewer yourself anymore! The whole system moved to vmprof.com and you can use it any time.

Sounds great. But what can you do with it? Here are two examples useful for a PyPy user:

PyPy crashed? Did you discover a bug?
-------------------

For some hard to find bugs it is often necessary to look at the compiled code. The old procedure often required to upload a plain text file which was hard to parse and to look through. 

The new way to share a crash report is to install the ``vmprof`` module from PyPi and execute either of the two commands:

```
# this program does not crash, but has some weird behaviour
$ pypy -m jitlog --web <your program args>
...
PyPy Jitlog: http://vmprof.com/#/<hash>
# this program segfaults
$ pypy -m jitlog -o /tmp/log <your program args>
...
<Segfault>
$ pypy -m jitlog --upload /tmp/log
PyPy Jitlog: http://vmprof.com/#/<hash>
```

Providing the link in the bug report enables PyPy developers browse and identify potential issues.

Speed issues
------------

VMProf is a great tool to find out hot spots that consume a lot of time in your program. As soon as you have idenified code that runs slow, you can switch to jitlog and maybe pin point certain aspects that do not behave as expected. You will find not only the overview, but are also able to browse the generated code. If you cannot make sense of that all you can just share the link with us and we can have a look at the compiled code.

Future direction
----------------

We hope that the new release will help both PyPy developers and PyPy users resolve potential issues and easily point them out.

Here are a few ideas what might come in the next few releases:

* Combination of CPU profiles and the JITLOG (Sadly did not make it into the current release)

* Extend vmprof.com to be able to query vmprof/jitlog. Some times it is interesting to search for specific patterns the compiler produced. An example for vmprof: 'methods.callsites() > 5' and for the jitlog would be 'traces.contains('call_assembler').hasbridge('*my_func_name*')'

* Extend the jitlog to capture the information of the optimization stage

Richard Plangger (plan_rich) and the PyPy team

