HippyVM - yet another attempt at PHP performance
------------------------------------------------

Who am I?
---------

* Maciej Fijalkowski

* PyPy developer for about 8 years

* main author of hippyvm

* founder of baroquesoftware.com

This talk
---------

* hippyvm project

* performance and measurments

* history

* questions after each part

HippyVM
-------

* a PHP interpreter (essentially), runs php code

|pause|

* has a just in time compiler, which makes it fast

|pause|

* dual licensing, commercial and open source

HippyVM status
--------------

* runs a lot of PHP test suite

* misses a lot of builtin functions

* can kind of "run" wordpress, mediawiki, squirrelmail, getting there

* cgi, fastcgi (not open source)

* fast

HippyVM status - short
----------------------

* fast, compliant

* not quite ready

HippyVM - Python bridge
-----------------------

* demo

HippyVM - questions
-------------------

* ?

Let's talk about performance
----------------------------

* "I want my website to run faster"

* "I'm going to compare various languages, implementations"

|pause|

* "I'll use a recursive fibonacci function"

Performance - breakdown
-----------------------

* user code

* runtime

* IO, DB, ... - libraries and ecosystem

* non-trivial interactions between the pieces

Performance
-----------

* a very complex picture

* bottlenecks depend on the use case

* libraries, programmers, styles matter

Performance - let's try science
-------------------------------

* get a set of programs (small, medium, large)

* compare them

* don't use a single number

PHP performance
---------------

* number of requests per second

* loading the code

* accessing the DB

* gluing it all together

PHP performance landscape
-------------------------

* Zend PHP

* HHVM

* php-ng

* HippyVM

* other projects

Current HippyVM performance
---------------------------

* we can't really compare large things (mediawiki ~on par)

* small and medium between 2x faster - 2x slower than HHVM

|pause|

* very hand-wavy, but you really need to do it yourself

|pause|

* consider bottlenecks differ depending on implementation

Good benchmarking - example
---------------------------

* speed.pypy.org

* I strongly encourage people to come up with the same for PHP

Performance - personal opinions
-------------------------------

* the language should be easy **for a programmer**

* the language implementation can be complex

* libraries, patterns and the ecosystem matter for anything non-trivial

Performance - questions
-----------------------

* ?

HippyVM history
---------------

* started as a facebook research project

* got some funding to pursue as a commercial project

* an offspin of PyPy technology

PyPy
----

* a fast, compliant Python interpreter

* 0.5%-1% of Python market share

* a framework for building efficient interpreters

* 10 years of research

* fully Open Source, EU funded project

Let's go back 10 years
----------------------

* Python is (like PHP) a very complex language

* writing an interpreter is hard

* writing a just-in-time compiler is even harder

* we decided to write a framework instead

A typical example
-----------------

* interpreter, written in C++

* just in time compiler that repeats the semantics, written in C++,
  emits assembler

* another layer, e.g. a method JIT

|pause|

* becomes harder and harder to keep up with semantics

PyPy approach
-------------

* write an interpreter in machine-readable language

* just in time compiler gets generated from the description

* a lot of work once, but prevents a lot of problems

How well it works?
------------------

* HippyVM - 4 people, 1.5 years

* HHVM - 5 years, team of up to 20

|pause|

* a lot of effort is reusable

* Truffle is another example of a similar approach

Questions?
----------

* hippyvm.com

* baroquesoftware.com

* talk to me!
