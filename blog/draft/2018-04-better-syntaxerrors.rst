Improving SyntaxError in PyPy
==============================

Since about a year, my halftime job at the uni has been to teach non-CS students
to program in Python. While doing that, I have been trying to see what common
stumbling blocks are, for programmers that are just starting out. There are many
things that could be said here, but one theme that emerges are
hard-to-understand error messages. One source of such error messages,
particularly when starting out, are ``SyntaxErrors``.


PyPy's parser (mostly following the architecture of CPython) uses a
regular-expression-based tokenizer with some cleverness to deal with
indentation, and a simple LR(1) parser. Both of these components obviously
produce errors for invalid syntax, but the messages are not that great. Often,
the message is just "invalid syntax", without any hint of what exactly is wrong.
In the last couple of weeks I have invested a little bit of effor to make them a
tiny bit better. Here are some examples.

Missing Characters
++++++++++++++++++++

The first class of errors is when a token is missing, but there is only one
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


Parenthesis
++++++++++++++++++++++

Another source of errors are unmatched parenthesis. Here, PyPy has always had
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

The same is true for parenthesis that are never closed (the call to ``eval`` is
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
++++++++++++++

Obviously these are just some very simple cases, and there is still a lot of
room for improvement (one huge problem is that only a simple ``SyntaxError`` is
ever shown per parse attempt, but fixing that is rather hard).

If you have a favorite unhelpful SyntaxError message you love to hate, please
tell us in the comments and we might try to improve it. Other kinds of bad error
messages are also always welcome!
