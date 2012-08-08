#!/usr/bin/env python
"""
Parse and summarize the jit-summary data """

import csv
import optparse
import os
import re
import sys
from pypy.jit.metainterp.history import ConstInt
from pypy.jit.tool.oparser import parse
from pypy.rpython.lltypesystem import llmemory, lltype
from pypy.tool import logparser
from backenddata import collect_logfiles

def collect_data(dirname, logs):
    for exe, name, log in logs:
        path = os.path.join(dirname, log)
        logfile = logparser.parse_log_file(path)
        summary = logparser.extract_category(logfile, 'jit-summary')
        if len(summary) == 0:
            yield (exe, name, log, 'n/a', 'n/a')
        summary = summary[0].splitlines()
        for line in summary:
            if line.startswith('Total # of bridges'):
                bridges = line.split()[-1]
            elif line.startswith('opt guards'):
                guards = line.split()[-1]
        yield (exe, name, log, guards, bridges)


def main(path):
    logs = collect_logfiles(path)
    if os.path.isdir(path):
        dirname = path
    else:
        dirname = os.path.dirname(path)
    results = collect_data(dirname, logs)

    with file("logs/bridge_summary.csv", "w") as f:
        csv_writer = csv.writer(f)
        row = ["exe", "bench", "guards", "bridges"]
        csv_writer.writerow(row)
        print row
        for exe, bench, log, guards, bridges in results:
            row = [exe, bench, guards, bridges]
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
