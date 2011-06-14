#!/usr/bin/env python
""" Usage:

runner.py [-w warmup] [-n times] [-c compile_command] <file> <extra_args>

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
    parser.add_option('-c', dest='compile_command',
                      help='for *.c a compile command')
    options, args = parser.parse_args()
    try:
        import pypyjit
    except ImportError:
        pass
    else:
        pypyjit.set_param(trace_limit=20000)
    if args[0].endswith('.py'):
        mod = py.path.local(args[0]).pyimport()
        sys.stderr.write("warming up")
        func = getattr(mod, args[1])
        args = args[2:]
        for i in range(options.warmup):
            func(args)
            sys.stderr.write('.')
        sys.stderr.write("\n")
        print >>sys.stderr, "benchmarking"
        all = []
        for i in range(options.no):
            t0 = time.time()
            name = func(args)
            all.append(time.time() - t0)
            print >>sys.stderr, "Next:", all[-1]
    else:
        # not needed
        options.warmup = 0
        all = []
        l = options.compile_command.split(" ") + [args[0]]
        pipe = subprocess.Popen(l, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        pipe.wait()
        print >>sys.stderr, pipe.stdout.read()
        print >>sys.stderr, pipe.stderr.read()
        for i in range(options.no):
            pipe = subprocess.Popen(['/usr/bin/time', '-f', '%e', './a.out']
                                    + args[1:],
                                     stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
            pipe.wait()
            l = pipe.stderr.read().split(" ")
            v = float(l[-1].strip("\n"))
            all.append(v)
            name = l[0][:-1] # strip :
            print >>sys.stderr, "Next: %s" % (v,)

    print >>sys.stderr, "benchmarked", name
    if options.no > 1:
        avg = sum(all) / len(all)
        stddev = (sum([(i - avg) * (i - avg) for i in all]) / (len(all) - 1)) ** 0.5
        print "%s: %s +- %s" % (name, avg, stddev)
    else:
        print "%s: %s" % (name, all[0])

if __name__ == '__main__':
    main()
