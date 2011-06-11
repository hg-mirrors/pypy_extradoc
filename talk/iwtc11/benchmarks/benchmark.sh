#!/bin/sh

echo
echo $*
if [ $1 == "gcc" ]; then
    $* sqrt/sqrt_double.c; /usr/bin/time -f %e ./a.out > /dev/null
    $* sqrt/sqrt_long.c; /usr/bin/time -f %e ./a.out > /dev/null
    $* sqrt/sqrt_fix16.c; /usr/bin/time -f %e ./a.out > /dev/null
    $* convolution/conv3.c -lm; /usr/bin/time -f %e ./a.out 1 > /dev/null
    $* convolution/conv5.c -lm; /usr/bin/time -f %e ./a.out 1 > /dev/null
    $* convolution/conv3.c -lm; /usr/bin/time -f %e ./a.out 100 > /dev/null
    $* convolution/conv5.c -lm; /usr/bin/time -f %e ./a.out 100 > /dev/null
    $* convolution/conv3.c -lm; /usr/bin/time -f %e ./a.out 1000 > /dev/null
    $* convolution/conv5.c -lm; /usr/bin/time -f %e ./a.out 1000 > /dev/null
    $* convolution/conv3x3.cc -lstdc++; /usr/bin/time -f %e ./a.out 1000000 3 > /dev/null
    $* convolution/conv3x3.cc -lstdc++; /usr/bin/time -f %e ./a.out 1000 1000 > /dev/null
    $* convolution/dilate3x3.cc -lstdc++; /usr/bin/time -f %e ./a.out 1000 1000 > /dev/null
    rm a.out
else
    $* sqrt/time_sqrt.py float
    $* sqrt/time_sqrt.py int
    $* sqrt/time_sqrt.py Fix16
    $* convolution/time_conv.py 1
    $* convolution/time_conv.py 100
    $* convolution/time_conv.py 1000
    $* convolution/time_conv2d.py
    $* image/noborder.py NoBorderImagePadded
    $* image/noborder.py NoBorderImage
fi
