#!/bin/bash

echo
echo $*
if [ "$1" == "gcc" ]; then
    ./runner.py -n 5 -c "$*" sqrt/sqrt_double.c
    ./runner.py -n 5 -c "$*" sqrt/sqrt_long.c
    ./runner.py -n 5 -c "$*" sqrt/sqrt_fix16.c
    #./runner.py -n 5 -c "$* -lm" convolution/conv3.c 1
    #./runner.py -n 5 -c "$* -lm" convolution/conv5.c 1
    ./runner.py -n 5 -c "$* -lm" convolution/conv3.c 100
    ./runner.py -n 5 -c "$* -lm" convolution/conv5.c 100
    ./runner.py -n 5 -c "$* -lm" convolution/conv3.c 1000
    ./runner.py -n 5 -c "$* -lm" convolution/conv5.c 1000
    ./runner.py -n 5 -c "$* -lstdc++" convolution/conv3x3.cc 1000000 3
    ./runner.py -n 5 -c "$* -lstdc++" convolution/conv3x3.cc 1000 1000
    ./runner.py -n 5 -c "$* -lstdc++" convolution/dilate3x3.cc 1000 1000
    ./runner.py -n 5 -c "$* -lstdc++" image/sobel.cc 1000 1000
    rm a.out
else
    if [ "$1" == "python2.7" ]; then
        EXTRA_OPTS='-w 0 -n 1'
    fi
    if [ "$1" == "python2.6" ]; then
        EXTRA_OPTS='-w 1 -n 1'
    fi
    $* ./runner.py $EXTRA_OPTS sqrt/sqrt.py main int
    $* ./runner.py $EXTRA_OPTS sqrt/sqrt.py main float
    $* ./runner.py $EXTRA_OPTS sqrt/sqrt.py main Fix16
    #$* ./runner.py $EXTRA_OPTS convolution/convolution.py conv3 1
    #$* ./runner.py $EXTRA_OPTS convolution/convolution.py conv5 1
    $* ./runner.py $EXTRA_OPTS convolution/convolution.py conv3 100
    $* ./runner.py $EXTRA_OPTS convolution/convolution.py conv5 100
    $* ./runner.py $EXTRA_OPTS convolution/convolution.py conv3 1000
    $* ./runner.py $EXTRA_OPTS convolution/convolution.py conv5 1000
    $* ./runner.py $EXTRA_OPTS convolution/convolution.py conv3x3 1000000 3
    $* ./runner.py $EXTRA_OPTS convolution/convolution.py conv3x3 1000 1000
    $* ./runner.py $EXTRA_OPTS convolution/convolution.py dilate3x3 1000 1000
    $* ./runner.py $EXTRA_OPTS convolution/convolution.py sobel_magnitude 1000 1000
    #$* ./runner.py $EXTRA_OPTS image/noborder.py main NoBorderImagePadded
    #$* ./runner.py $EXTRA_OPTS image/noborder.py main NoBorderImagePadded iter
    #$* ./runner.py $EXTRA_OPTS image/noborder.py main NoBorderImagePadded range
    #$* ./runner.py $EXTRA_OPTS image/noborder.py main NoBorderImage
    #$* ./runner.py $EXTRA_OPTS image/noborder.py main NoBorderImage iter
    #$* ./runner.py $EXTRA_OPTS image/noborder.py main NoBorderImage range
    #$* ./runner.py $EXTRA_OPTS image/sobel.py main NoBorderImagePadded
    #$* ./runner.py $EXTRA_OPTS image/sobel.py main NoBorderImagePadded uint8
fi
