
=======================================
Software Transactional Memory with PyPy
=======================================


Introduction
------------

* what is PyPy: an alternative implementation of Python

* main focus is on speed


Introduction
------------

.. image: speed.png


SQL Databases by example
------------------------

::

    BEGIN TRANSACTION;
    SELECT * FROM ...;
    UPDATE ...;
    COMMIT;


Python by example
-----------------

::

    ..
    x = obj.value
    obj.value = x + 1
    ..


Python by example
-----------------

::

    begin_transaction()
    x = obj.value
    obj.value = x + 1
    commit_transaction()


Python by example
-----------------

::

    with atomic:
        x = obj.value
        obj.value = x + 1


Python by example
-----------------

::

    with the_lock:
        x = obj.value
        obj.value = x + 1


Locks != Transactions
---------------------

::

    BEGIN TRANSACTION;    BEGIN TRANSACTION;    BEGIN..
    SELECT * FROM ...;    SELECT * FROM ...;    SELEC..
    UPDATE ...;           UPDATE ...;           UPDAT..
    COMMIT;               COMMIT;               COMMI..


Locks != Transactions
---------------------

::

    with the_lock:        with the_lock:        with ..
      x = obj.val           x = obj.val           x =..
      obj.val = x + 1       obj.val = x + 1       obj..


Locks != Transactions
---------------------

::

    with atomic:          with atomic:          with ..
      x = obj.val           x = obj.val           x =..
      obj.val = x + 1       obj.val = x + 1       obj..


STM
---

* Transactional Memory

* advanced magic (but not more so than databases)


STM versus HTM
--------------

* Software versus Hardware

* CPU hardware specially to avoid the high overhead

* too limited for now


Example 1
---------

::

  def apply_interest_rate(self):
     self.balance *= 1.05

  for account in all_accounts:
     account.apply_interest_rate()


Example 1
---------

::

  def apply_interest_rate(self):
     self.balance *= 1.05

  for account in all_accounts:
     add_task(account.apply_interest_rate)
  run_tasks()


Internally
----------

* `run_all_tasks()` manages a pool of threads

* each thread runs tasks in a `with atomic`


Example 2
---------

::

  def next_iteration(all_trains):
     for train in all_trains:
        start_time = ...
        for othertrain in train.dependencies:
           if ...:
              start_time = ...
        train.start_time = start_time


Example 2
---------

::

  def compute(train):
     ...

  def next_iteration(all_trains):
     for train in all_trains:
        add_task(compute, train)
     run_all_tasks()


By the way
----------

* STM replaces the GIL

* any existing multithreaded program runs on multiple cores


Current status
--------------

* 



User feedback
-------------

::

  Detected conflict:
    File "foo.py", line 17, in walk
      if node.left not in seen:
  Transaction aborted, 0.000047 seconds lost


User feedback
-------------

::

  Forced inevitable:
    File "foo.py", line 19, in walk
      print >> log, logentry
  Transaction blocked others for 0.xx seconds

(not implemented yet)
