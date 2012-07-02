.. include:: beamerdefs.txt

================================
PyPy JIT under the hood
================================

About this talk
----------------

* What is PyPy? (in 30 seconds)

  - (for those who missed the keynote :-))

* Overview of tracing JITs

* The PyPy JIT generator

* JIT-friendly programs


Part 0: What is PyPy?
----------------------

* RPython toolchain

  - subset of Python

  - ideal for writing VMs

  - JIT & GC for free

* Python interpreter

  - written in RPython

* Whatever (dynamic) language you want

  - smalltalk, prolog, javascript, ...


Part 1
------

**Overview of tracing JITs**

Compilers
---------

* When?

  - Batch or Ahead Of Time

  - Just In Time

|pause|

* How?

  - Static

  - Dynamic or Adaptive

|pause|

* What?

  - Method-based compiler

  - Tracing compiler

|pause|

* PyPy: JIT, Dynamic, Tracing


Assumptions
-----------

* Pareto Principle (80-20 rule)

  - the 20% of the program accounts for the 80% of the runtime

  - **hot-spots**

* Fast Path principle

  - optimize only what is necessary

  - fall back for uncommon cases

|pause|

* Most of runtime spent in **loops**

* Always the same code paths (likely)


Tracing JIT
-----------

* Interpret the program as usual

* Detect **hot** loops

* Tracing phase

  - **linear** trace

* Compiling

* Execute

  - guards to ensure correctness

* Profit :-)


Tracing JIT phases
-------------------

.. animage:: diagrams/tracing-phases-p*.pdf
   :align: center
   :scale: 100%


Tracing Example (1)
--------------------

.. we use java instead of RPython to avoid confusion with applevel Python


|scriptsize|
|example<| |small| java |end_small| |>|

.. sourcecode:: java

    interface Operation {
        int DoSomething(int x);
    }
    class IncrOrDecr implements Operation {
        public int DoSomething(int x) { 
            if (x < 0) return x-1;
            else       return x+1;
        }
    }
    class tracing {
        public static void main(String argv[]) {
            int N = 100;
            int i = 0;
            Operation op = new IncrOrDecr();
            while (i < N) {
                i = op.DoSomething(i);
            }
            System.out.println(i);
        }
    }

|end_example|
|end_scriptsize|


Tracing Example (2)
--------------------

|scriptsize|
|column1|
|example<| |small| Java bytecode |end_small| |>|

.. sourcecode:: java

  class IncrOrDecr {
    ...
    public DoSomething(I)I
      ILOAD 1
      IFGE LABEL_0
      ILOAD 1
      ICONST_1
      ISUB
      IRETURN
     LABEL_0
      ILOAD 1
      ICONST_1
      IADD
      IRETURN
  }

|end_example|

|pause|

|column2|
|example<| |small| Java bytecode |end_small| |>|

.. sourcecode:: java

  class tracing {
    ...
    public static main(
       [Ljava/lang/String;)V
      ...
     LABEL_0
      ILOAD 2
      ILOAD 1
      IF_ICMPGE LABEL_1
      ALOAD 3
      ILOAD 2
      INVOKEINTERFACE 
        Operation.DoSomething (I)I
      ISTORE 2
      GOTO LABEL_0
     LABEL_1
      ...
  }

|end_example|
|end_columns|
|end_scriptsize|


Tracing example (3)
-------------------

.. animage:: diagrams/trace-p*.pdf
   :align: center
   :scale: 80%
