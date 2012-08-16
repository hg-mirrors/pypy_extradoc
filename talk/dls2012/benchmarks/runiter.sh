#!/bin/sh

BENCHMARKS="sum1d  sum2d  whsum2d  wsum1d  wsum2d  xsum1d  xsum2d  xysum2d mean1d median1d ripple1d ripple2d"
echo gcc -O3
for b in $BENCHMARKS; do
    ./runner.py -n 5 -c "gcc -O3" iter/$b.c 10
done
echo

for p in iter/*.py; do
    echo pypy $p
    for b in $BENCHMARKS; do
	/tmp/pypy-trunk ./runner.py -n 5 $p $b 10
    done
    echo
done