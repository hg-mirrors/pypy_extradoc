#!/usr/bin/env python
"""
Parse and summarize the jit-summary data """

import optparse
import os
import re
import sys
import json
from pypy.jit.metainterp.history import ConstInt
from pypy.jit.tool.oparser import parse
from pypy.rpython.lltypesystem import llmemory, lltype
from pypy.tool import logparser
from backenddata import collect_logfiles

def collect_data(dirname, logs):
    for exe, bench, log in logs:
        path = os.path.join(dirname, log)
        logfile = logparser.parse_log_file(path)
        counts = {}
        guard_failures = \
            logparser.extract_category(logfile, 'jit-guard-failure')
        backend_counts = \
            logparser.extract_category(logfile, 'jit-backend-counts')

        assert len(guard_failures) > 0
        assert len(backend_counts) > 0
        # collect guard failures first
        for g in guard_failures:
            name = g.split(' ')[1].strip()
            counts.setdefault(name, 0)
            counts[name] += 1
        for i in backend_counts:
            if i == '':
                continue
            for l in i.splitlines():
                if not l.startswith('bridge'):
                    continue
                colon = l.index(':')
                n = l[len('bridge '):colon]
                count = int(l[colon+1:])
                counts[n] += count
        yield (exe, bench, counts)


def main(path):
    logs = collect_logfiles(path)
    if os.path.isdir(path):
        dirname = path
    else:
        dirname = os.path.dirname(path)
    results = collect_data(dirname, logs)
    data = {}
    for exe, bench, guards in results:
        data[bench] = {'exe': exe, 'results': guards}
    with file("logs/guard_summary.json", "w") as f:
        print >>f, json.dumps(data, f, sort_keys=True, indent=4)

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog logdir_or_file")

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(2)
    else:
        main(args[0])
