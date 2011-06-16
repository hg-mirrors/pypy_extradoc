#!/bin/bash

./benchmark.sh pypy
#./benchmark.sh pypy --jit enable_opts=intbounds:rewrite:virtualize:heap:unroll
./benchmark.sh pypy --jit enable_opts=intbounds:rewrite:virtualize:heap
#./benchmark.sh gcc
./benchmark.sh gcc -O2
./benchmark.sh gcc -O3 -march=native -fno-tree-vectorize
./benchmark.sh python2.7
./benchmark.sh python2.6 psyco-wrapper.py
