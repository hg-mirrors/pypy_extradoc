#!/usr/bin/env python
"""
Parse and summarize the traces produced by pypy-c-jit when PYPYLOG is set.
only works for logs when unrolling is disabled
"""

import py
import os
import sys
import csv
import optparse
from pprint import pprint
from pypy.tool import logparser
from pypy.jit.tool.oparser import parse
from pypy.jit.metainterp.history import ConstInt
from pypy.rpython.lltypesystem import llmemory, lltype

categories = {
    'setfield_gc': 'set',
    'setarrayitem_gc': 'set',
    'strsetitem': 'set',
    'getfield_gc': 'get',
    'getfield_gc_pure': 'get',
    'getarrayitem_gc': 'get',
    'getarrayitem_gc_pure': 'get',
    'strgetitem': 'get',
    'new': 'new',
    'new_array': 'new',
    'newstr': 'new',
    'new_with_vtable': 'new',
}

all_categories = 'new get set guard numeric rest'.split()

def extract_opnames(loop):
    loop = loop.splitlines()
    for line in loop:
        if line.startswith('#') or line.startswith("[") or "end of the loop" in line:
            continue
        frontpart, paren, _ = line.partition("(")
        assert paren
        if " = " in frontpart:
            yield frontpart.split(" = ", 1)[1]
        elif ": " in frontpart:
            yield frontpart.split(": ", 1)[1]
        else:
            yield frontpart

def summarize(loop, adding_insns={}):    # for debugging
    insns = adding_insns.copy()
    seen_label = True
    if "label" in loop:
        seen_label = False
    for opname in extract_opnames(loop):
        if not seen_label:
            if opname == 'label':
                seen_label = True
            else:
                assert categories.get(opname, "rest") == "get"
                continue
        if opname.startswith("int_") or opname.startswith("float_"):
            opname = "numeric"
        elif opname.startswith("guard_"):
            opname = "guard"
        else:
            opname = categories.get(opname, 'rest')
        insns[opname] = insns.get(opname, 0) + 1
    assert seen_label
    return insns

def compute_summary_diff(loopfile, options):
    print loopfile
    log = logparser.parse_log_file(loopfile)
    loops, summary = consider_category(log, options, "jit-log-opt-")

    # non-optimized loops and summary
    nloops, nsummary = consider_category(log, options, "jit-log-noopt-")
    diff = {}
    keys = set(summary.keys()).union(set(nsummary))
    for key in keys:
        before = nsummary[key]
        after = summary[key]
        diff[key] = (before-after, before, after)
    return len(loops), summary, diff

def main(loopfile, options):
    _, summary, diff = compute_summary_diff(loopfile, options)

    print
    print 'Summary:'
    print_summary(summary)

    if options.diff:
        print_diff(diff)

def consider_category(log, options, category):
    loops = logparser.extract_category(log, category)
    if options.loopnum is None:
        input_loops = loops
    else:
        input_loops = [loops[options.loopnum]]
    summary = dict.fromkeys(all_categories, 0)
    for loop in loops:
        summary = summarize(loop, summary)
    return loops, summary


def print_summary(summary):
    ops = [(summary[key], key) for key in summary]
    ops.sort(reverse=True)
    for n, key in ops:
        print '%5d' % n, key

def print_diff(diff):
    ops = [(key, before, after, d) for key, (d, before, after) in diff.iteritems()]
    ops.sort(reverse=True)
    tot_before = 0
    tot_after = 0
    print ",",
    for key, before, after, d in ops:
        print key, ", ,",
    print "total"
    print args[0], ",",
    for key, before, after, d in ops:
        tot_before += before
        tot_after += after
        print before, ",", after, ",",
    print tot_before, ",", tot_after

def mainall(options):
    logs = os.listdir("logs")
    all = []
    for log in logs:
        parts = log.split(".")
        if len(parts) != 3:
            continue
        l, exe, bench = parts
        if l != "logbench":
            continue
        all.append((exe, bench, log))
    all.sort()
    with file("logs/summary.csv", "w") as f:
        csv_writer = csv.writer(f)
        row = ["exe", "bench", "number of loops"]
        for cat in all_categories:
            row.append(cat + " before")
            row.append(cat + " after")
        csv_writer.writerow(row)
        print row
        for exe, bench, log in all:
            num_loops, summary, diff = compute_summary_diff("logs/" + log, options)
            print diff
            print exe, bench, summary
            row = [exe, bench, num_loops]
            for cat in all_categories:
                difference, before, after = diff[cat]
                row.append(before)
                row.append(after)
            csv_writer.writerow(row)
            print row

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog loopfile [options]")
    parser.add_option('-n', '--loopnum', dest='loopnum', default=None, metavar='N', type=int,
                      help='show the loop number N [default: last]')
    parser.add_option('-a', '--all', dest='loopnum', action='store_const', const=None,
                      help='show all loops in the file')
    parser.add_option('-d', '--diff', dest='diff', action='store_true', default=False,
                      help='print the difference between non-optimized and optimized operations in the loop(s)')
    parser.add_option('--diffall', dest='diffall', action='store_true', default=False,
                      help='diff all the log files around')

    options, args = parser.parse_args()
    if options.diffall:
        mainall(options)
    elif len(args) != 1:
        parser.print_help()
        sys.exit(2)
    else:
        main(args[0], options)
