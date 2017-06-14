Why is Python slow?
===================

In this talk, I will cover one of the usual topics of discussions
of deficiencies of the Python language, notably it's speed. We've spend
last decade improving on the performance of the language (but not the default
implementation). What we've learned so far is not what's the common
interpretation of that question - things like dynamic dispatch, dynamic
typing and interpreter can all be worked around. What we learned are the
places in the Python language which make unnecessary string copies, but
are easier to write, a lot of "pythonic" constructs that cannot be implemented
efficiently and a lot of quirks that make some constructs slow for no good
reason. Additionally we're overwhelmed by the sheer size of the "simple"
language and the necessity of supporting C extensions. This talk will cover
detailed view of those problems and some potential remedies.