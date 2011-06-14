#!/bin/bash

echo
echo $*
if [ "$1" == "gcc" ]; then
    ./runner.py -n 5 -c "$*" sqrt/sqrt_double.c
    ./runner.py -n 5 -c "$*" sqrt/sqrt_long.c
    ./runner.py -n 5 -c "$*" sqrt/sqrt_fix16.c
    ./runner.py -n 5 -c "$* -lm" convolution/conv3.c 1
    ./runner.py -n 5 -c "$* -lm" convolution/conv5.c 1
    ./runner.py -n 5 -c "$* -lm" convolution/conv3.c 100
    ./runner.py -n 5 -c "$* -lm" convolution/conv5.c 100
    ./runner.py -n 5 -c "$* -lm" convolution/conv3.c 1000
    ./runner.py -n 5 -c "$* -lm" convolution/conv5.c 1000
    ./runner.py -n 5 -c "$* -lstdc++" convolution/conv3x3.cc 1000000 3
    ./runner.py -n 5 -c "$* -lstdc++" convolution/conv3x3.cc 1000 1000
    ./runner.py -n 5 -c "$* -lstdc++" convolution/dilate3x3.cc 1000 1000
    ./runner.py -n 5 -c "$* -lstdc++" image/sobel.cc 1002 1002
    rm a.out
else
    #./runner.py -n 10 sqrt/sqrt.py main int
    #./runner.py -n 10 sqrt/sqrt.py main float
    #./runner.py -n 10 sqrt/sqrt.py main Fix16
    ./runner.py convolution/convolution.py conv3 1
    ./runner.py convolution/convolution.py conv3 100
    ./runner.py convolution/convolution.py conv3 1000

#    $* sqrt/time_sqrt.py float
#    $* sqrt/time_sqrt.py int
#    $* sqrt/time_sqrt.py Fix16
#    $* convolution/time_conv.py 1
#    $* convolution/time_conv.py 100
#    $* convolution/time_conv.py 1000
#    $* convolution/time_conv2d.py
#    $* image/noborder.py NoBorderImagePadded
#    $* image/noborder.py NoBorderImage
#    $* image/time_sobel.py NoBorderImagePadded
fi
