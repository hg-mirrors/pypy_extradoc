#!/usr/bin/env python
""" Usage:

runner.py [-w warmup] [-n times] <file> <extra_args>

Where extra_args is either what you pass to python file, if file ends with .py
or a C compiler and it's options
"""

from __future__ import division

import py
import sys
import time
from optparse import OptionParser
import subprocess

def main():
    parser = OptionParser()
    parser.add_option('-n', dest='no', help='number of iterations', type=int,
                      default=10)
    parser.add_option('-w', dest='warmup', help='number of warmup runs',
                      type=int, default=3)
    options, args = parser.parse_args()
    if args[0].endswith('.py'):
        mod = py.path.local(args[0]).pyimport()
        sys.stderr.write("warming up")
        args = args[1:]
        for i in range(options.warmup):
            mod.main(args)
            sys.stderr.write('.')
        sys.stderr.write("\n")
        print >>sys.stderr, "benchmarking"
        all = []
        for i in range(options.no):
            t0 = time.time()
            mod.main(args)
            all.append(time.time() - t0)
            print >>sys.stderr, "Next:", all[-1]
        name = mod.name
    else:
        # not needed
        options.warmup = 0
        all = []
        pipe = subprocess.Popen(args[1:] + [args[0]])
        pipe.wait()
        for i in range(options.no):
            pipe = subprocess.Popen(['/usr/bin/time', '-f', '%e', './a.out'],
                                     stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
            pipe.wait()
            v = float(pipe.stderr.read().strip("\n"))
            all.append(v)
            print >>sys.stderr, "Next: %s" % (v,)
        name = args[0].split(".")[0].split("/")[-1]
        
    if options.no > 1:
        avg = sum(all) / len(all)
        stddev = (sum([(i - avg) * (i - avg) for i in all]) / (len(all) - 1)) ** 0.5
        print "%s: %s +- %s" % (name, avg, stddev)
    else:
        print "%s: %s" % (name, all[0])

if __name__ == '__main__':
    main()
