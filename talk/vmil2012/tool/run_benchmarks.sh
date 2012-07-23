#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
base="$(dirname "${DIR}")"
bench_list="${base}/logs/benchs.txt"
benchmarks="${base}/pypy-benchmarks"
REV="ff7b35837d0f"
pypy=$(which pypy)
pypy_opts=",--jit enable_opts=intbounds:rewrite:virtualize:string:pure:heap:ffi"
baseline=$(which true)

# setup a checkout of the pypy benchmarks and update to a fixed revision
if [ ! -d "${benchmarks}" ]; then
  echo "Cloning pypy/benchmarks repository to ${benchmarks}"
  hg clone https://bitbucket.org/pypy/benchmarks "${benchmarks}"
  cd "${benchmarks}"
  echo "updating benchmarks to fixed revision ${REV}"
  hg update "${REV}"
  echo "Patching benchmarks to pass PYPYLOG to benchmarks"
  patch -p1 < "$base/tool/env.patch" 
else
  cd "${benchmarks}"
  echo "Clone of pypy/benchmarks already present, reverting changes in the checkout"
  hg revert --all
  echo "updating benchmarks to fixed revision ${REV}"
  hg update "${REV}"
  echo "Patching benchmarks to pass PYPYLOG to benchmarks"
  patch -p1 < "$base/tool/env.patch" 
fi

# run each benchmark defined on $bench_list
while read line
do
    logname="${base}/logs/logbench.$(basename "${pypy}").${line}"
    export PYPYLOG="jit:$logname"
    bash -c "./runner.py --fast --changed=\"${pypy}\" --args=\"${pypy_opts}\" --benchmarks=${line}"
done < $bench_list
