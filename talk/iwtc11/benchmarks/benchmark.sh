#!/bin/sh

echo
echo $*
if [ $1 == "gcc" ]; then
    $* sqrt/sqrt_double.c; /usr/bin/time -f %e ./a.out > /dev/null
    $* sqrt/sqrt_long.c; /usr/bin/time -f %e ./a.out > /dev/null
    $* sqrt/sqrt_fix16.c; /usr/bin/time -f %e ./a.out > /dev/null
    rm a.out
else
    $* sqrt/time_sqrt.py float
    $* sqrt/time_sqrt.py int
    $* sqrt/time_sqrt.py Fix16
fi
