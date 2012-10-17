In this talk I would like to present the dominant implementation of Python
(CPython) performance characteristics and explain why, in case the performance
is an issue for your application, its characteristics are bad for
abstractions.

In the next part I'll explain the mission statement of the PyPy Python
implementation, brief description of its performance characteristics and
where the project is going. I'll also explain the basics of Just in Time
compilation and what it changes on the observed performance.
In summary, the goal is to explain how
"if you want performance, don't write things in Python" is a bad attitude
and how we're trying to battle it with a high performance Python
virtual machine.
