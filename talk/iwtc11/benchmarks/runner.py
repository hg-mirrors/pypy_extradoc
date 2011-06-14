#!/usr/bin/env python
""" Usage:

runner.py [-w warmup] [-n times] <file> <extra_args>
"""

from __future__ import division

import py
import sys
import time
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option('-n', dest='no', help='number of iterations', type=int,
                      default=10)
    parser.add_option('-w', dest='warmup', help='number of warmup runs',
                      type=int, default=0)
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
    else:
        
    if n > 1:
        avg = sum(all) / len(all)
        stddev = (sum([(i - avg) * (i - avg) for i in all]) / (len(all) - 1)) ** 0.5
        print "Avg: %s +- %s" % (avg, stddev)
    else:
        print "Run: %s" % (all[0],)

if __name__ == '__main__':
    main()
