#!/bin/bash

# invoke like
#    ./measure_memusage.sh command to execute
# it uses 'top' and records its output in a tempfile (not deleted
# afterwards). The interval for measurements is 1s. The RES/VIRT/SHR
# should be in KiB.

TMPFILE=$(tempfile)

"$@" &
PID=$!

top -d1 -b -i -p $PID > $TMPFILE &
MEMPID=$!

wait $PID
kill $MEMPID

cat $TMPFILE | egrep "(PID)|(^\W*$PID)"
echo "RESULTS in $TMPFILE"
#pypy-c ~/pypy/benchmarks/multithread/multithread-richards.py 100 4 2>/dev/null & top -d1 -b -i -p $(pidof pypy-c)  > output
