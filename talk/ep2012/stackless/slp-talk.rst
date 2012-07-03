.. include:: beamerdefs.txt

============================================
The Story of Stackless Python
============================================

What is Stackless about?
-------------------------

* it is like CPython

|pause|

* it can do a little bit more

|pause|

* adds a single module

|pause|

|scriptsize|
|example<| |>|

  .. sourcecode:: python
  
    import stackless
    
|end_example|
|end_scriptsize|

|pause|

* is like an extension

  - but, sadly, not really
  
  - **but:** there is a solution...


Now, what is it really about?
------------------------------

* have tiny little "main" programs

  - ``tasklet``
  
|pause|

* tasklets communicate via messages

  - ``channel``
  
|pause|

* tasklets are often called ``microthreads``

  - but there are no threads at all
  
  - only one tasklets runs at any time

|pause|

* *but see the PyPy STM* approach

  - this will apply to tasklets as well

Cooperative Multitasking ...
-------------------------------

|scriptsize|
|example<| |>|

  .. sourcecode:: pycon
  
    >>> import stackless
    >>>
    >>> channel = stackless.channel()
    
|pause|

  .. sourcecode:: pycon

    >>> def receiving_tasklet():
    ...     print "Receiving tasklet started"
    ...     print channel.receive()
    ...     print "Receiving tasklet finished"
    ...

|pause|

  .. sourcecode:: pycon

    >>> def sending_tasklet():
    ...     print "Sending tasklet started"
    ...     channel.send("send from sending_tasklet")
    ...     print "sending tasklet finished"
    ...

|end_example|
|end_scriptsize|


Cooperative Multitasking ...
-------------------------------

|scriptsize|
|example<| |>|

  .. sourcecode:: pycon

    >>> def another_tasklet():
    ...     print "Just another tasklet in the scheduler"
    ...

|pause|

  .. sourcecode:: pycon

    >>> stackless.tasklet(receiving_tasklet)()
    <stackless.tasklet object at 0x00A45B30>
    >>> stackless.tasklet(sending_tasklet)()
    <stackless.tasklet object at 0x00A45B70>
    >>> stackless.tasklet(another_tasklet)()
    <stackless.tasklet object at 0x00A45BF0>
    
|end_example|
|end_scriptsize|


... Cooperative Multitasking
-------------------------------

|scriptsize|
|example<| |>|
    
  .. sourcecode:: pycon

    <stackless.tasklet object at 0x00A45B70>
    >>> stackless.tasklet(another_tasklet)()
    <stackless.tasklet object at 0x00A45BF0>
    >>>
    >>> stackless.run()
    Receiving tasklet started
    Sending tasklet started
    send from sending_tasklet
    Receiving tasklet finished
    Just another tasklet in the scheduler
    sending tasklet finished

|end_example|
|end_scriptsize|


Why not just the *greenlet* ?
-------------------------------

* greenlets are a subset of stackless

  - there is no scheduler
  
  - can emulate stackless
  
|pause|

* greenlets are about 5-10x slower to switch

  using only hard-switching
  
|pause|

* but the main difference is ...


Pickling Program State
-----------------------

|scriptsize|
|example<| Example (p. 1 of 2) |>|

  .. sourcecode:: python

    import pickle, sys
    import stackless
    
    ch = stackless.channel()
    
    def recurs(depth, level=1):
        print 'enter level %s%d' % (level*'  ', level)
        if level >= depth:
            ch.send('hi')
        if level < depth:
            recurs(depth, level+1)
        print 'leave level %s%d' % (level*'  ', level)

|end_example|
|end_scriptsize|


Pickling Program State
-----------------------

|scriptsize|

|example<| Example (p. 2 of 2) |>|

  .. sourcecode:: python


    def demo(depth):
        t = stackless.tasklet(recurs)(depth)
        print ch.receive()
        pickle.dump(t, file('tasklet.pickle', 'wb'))
    
    if __name__ == '__main__':
        if len(sys.argv) > 1:
            t = pickle.load(file(sys.argv[1], 'rb'))
            t.insert()
        else:
            t = stackless.tasklet(demo)(9)
        stackless.run()

    # remember to show it interactively

|end_example|
|end_scriptsize|


Software archeology
-------------------

* Around since 1998

  - version 1
  
    - using only soft-switching
    
    - continuation-based
  
    - *please let me skip old design errors :-)*

* Complete redesign in 2002

  - version 2
  
    - using only hard-switching
    
    - birth of tasklets and channels
    
* Concept merge in 2004

  - version 3
  
    - **80-20** rule:
    
    - soft-switching whenever possible
      
    - hard-switching if foreign code is on the stack
      
  * these 80 % can be *pickled*

Thank you
---------

* http://pypy.org/

* You can hire Antonio

* Questions?
