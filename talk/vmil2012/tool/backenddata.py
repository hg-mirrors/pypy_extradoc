#!/usr/bin/env python
"""
Parse and summarize the traces produced by pypy-c-jit when PYPYLOG is set.
only works for logs when unrolling is disabled
"""

import csv
import optparse
import os
import re
import sys
from pypy.jit.metainterp.history import ConstInt
from pypy.jit.tool.oparser import parse
from pypy.rpython.lltypesystem import llmemory, lltype
from pypy.tool import logparser


def collect_logfiles(path):
    if not os.path.isdir(path):
        logs = [os.path.basename(path)]
    else:
        logs = os.listdir(path)
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
    return all


def collect_guard_data(log):
    """Calculate the total size in bytes of the locations maps for all guards
    in a logfile"""
    guards = logparser.extract_category(log, 'jit-backend-guard-size')
    return sum(int(x[6:]) for x in guards if x.startswith('chars'))


def collect_asm_size(log, guard_size=0):
    """Calculate the size of the machine code pieces of a logfile. If
    guard_size is passed it is substracted from result under the assumption
    that the guard location maps are encoded in the instruction stream"""
    asm = logparser.extract_category(log, 'jit-backend-dump')
    asmlen = 0
    for block in asm:
        expr = re.compile("CODE_DUMP @\w+ \+\d+\s+(.*$)")
        match = expr.search(block)
        assert match is not None  # no match found
        code = match.group(1)
        asmlen += len(code)
    return asmlen - guard_size


def collect_data(dirname, logs):
    for exe, name, log in logs:
        path = os.path.join(dirname, log)
        logfile = logparser.parse_log_file(path)
        guard_size = collect_guard_data(logfile)
        asm_size = collect_asm_size(logfile, guard_size)
        yield (exe, name, log, asm_size, guard_size)


def main(path):
    logs = collect_logfiles(path)
    if os.path.isdir(path):
        dirname = path
    else:
        dirname = os.path.dirname(path)
    results = collect_data(dirname, logs)

    with file("logs/backend_summary.csv", "w") as f:
        csv_writer = csv.writer(f)
        row = ["exe", "bench", "asm size", "guard map size"]
        csv_writer.writerow(row)
        print row
        for exe, bench, log, asm_size, guard_size in results:
            row = [exe, bench, asm_size / 1024, guard_size / 1024]
            csv_writer.writerow(row)
            print row

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog logdir_or_file")

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(2)
    else:
        main(args[0])
