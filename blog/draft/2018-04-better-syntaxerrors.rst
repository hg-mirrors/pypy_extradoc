Improving SyntaxError in PyPy
==============================

For the last year, my halftime job has been to teach non-CS uni students
to program in Python. While doing that, I have been trying to see what common
stumbling blocks exist for novice programmers. There are many
things that could be said here, but a common theme that emerges is
hard-to-understand error messages. One source of such error messages,
particularly when starting out, is ``SyntaxErrors``.

PyPy's parser (mostly following the architecture of CPython) uses a
regular-expression-based tokenizer with some cleverness to deal with
indentation, and a simple LR(1) parser. Both of these components obviously
produce errors for invalid syntax, but the messages are not very helpful. Often,
the message is just "invalid syntax", without any hint of what exactly is wrong.
In the last couple of weeks I have invested a little bit of effort to make them a
tiny bit better. They will be part of the upcoming PyPy 6.0 release. Here are
some examples of what changed.

Missing Characters
++++++++++++++++++

The first class of errors occurs when a token is missing, often there is only one
valid token that the parser expects. This happens most commonly by leaving out
the ':' after control flow statements (which is the syntax error I personally
still make at least a few times a day). In such situations, the parser will now
tell you which character it expected:

.. sourcecode:: pycon

    >>>> # before
    >>>> if 1
      File "<stdin>", line 1
        if 1
           ^
    SyntaxError: invalid syntax
    >>>> 

    >>>> # after
    >>>> if 1
      File "<stdin>", line 1
        if 1
           ^
    SyntaxError: invalid syntax (expected ':')
    >>>> 

Another example of this feature:

.. sourcecode:: pycon

    >>>> # before
    >>>> def f:
      File "<stdin>", line 1
        def f:
            ^
    SyntaxError: invalid syntax
    >>>>

    >>>> # after
    >>>> def f:
      File "<stdin>", line 1
        def f:
             ^
    SyntaxError: invalid syntax (expected '(')
    >>>> 


Parentheses
+++++++++++

Another source of errors are unmatched parentheses. Here, PyPy has always had
slightly better error messages than CPython:

.. sourcecode:: pycon

    >>> # CPython
    >>> )
      File "<stdin>", line 1
        )
        ^
    SyntaxError: invalid syntax
    >>> 

    >>>> # PyPy
    >>> )
      File "<stdin>", line 1
        )
        ^
    SyntaxError: unmatched ')'
    >>>> 

The same is true for parentheses that are never closed (the call to ``eval`` is
needed to get the error, otherwise the repl will just wait for more input):

.. sourcecode:: pycon

    >>> # CPython
    >>> eval('(')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<string>", line 1
        (
        ^
    SyntaxError: unexpected EOF while parsing
    >>>

    >>>> # PyPy
    >>>> eval('(')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<string>", line 1
        (
        ^
    SyntaxError: parenthesis is never closed
    >>>>


What I have now improved is the case of parenthesis that are matched wrongly:

.. sourcecode:: pycon

    >>>> # before
    >>>> (1,
    .... 2,
    .... ]
      File "<stdin>", line 3
        ]
        ^
    SyntaxError: invalid syntax
    >>>> 

    >>>> # after
    >>>> (1,
    .... 2,
    .... ]
      File "<stdin>", line 3
        ]
        ^
    SyntaxError: closing parenthesis ']' does not match opening parenthesis '(' on line 1
    >>>> 


Conclusion
++++++++++

Obviously these are just some very simple cases, and there is still a lot of
room for improvement (one huge problem is that only a simple ``SyntaxError`` is
ever shown per parse attempt, but fixing that is rather hard).

If you have a favorite unhelpful SyntaxError message you love to hate, please
tell us in the comments and we might try to improve it. Other kinds of
non-informative error messages are also always welcome!
