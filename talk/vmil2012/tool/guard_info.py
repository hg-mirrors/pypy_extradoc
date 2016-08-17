from pypy.tool import logparser
from backenddata import collect_logfiles
import json
import os
import optparse
import sys


def extract_guards(dirname, logs):
    for exe, bench, log in logs:
        path = os.path.join(dirname, log)
        logfile = logparser.parse_log_file(path)
        guarddata = [line
                for sec in logparser.extract_category(logfile, 'jit-log-opt')
                    for line in sec.splitlines()
                        if line.find('<Guard') >= 0]
        yield bench, guarddata


def extract_guard_name(logline):
    return logline[logline.index('guard'):logline.index('(')].strip()


def get_failure_info(results, guards):
    guards_by_failure = sorted(results.iteritems(),
                            key=lambda x: x[1],
                            reverse=True)

    for guard, failures in guards_by_failure:
        g = [x for x in guards if x.find('Guard%s>' % guard) >= 0]
        if len(g) != 1:
            print "Uhhh", g

        g = g[0]
        yield failures, guard, extract_guard_name(g)


def main(path):
    logs = collect_logfiles(path)
    if os.path.isdir(path):
        dirname = path
    else:
        dirname = os.path.dirname(path)
    results = extract_guards(dirname, logs)
    with file("logs/guard_summary.json") as f:
        failure_info = json.load(f)
    with file("logs/guard_failure_data.txt", "w") as f:
        for bench, guards in results:
            print >>f, "Benchmark", bench
            for failures, guard, data in \
                get_failure_info(failure_info[bench]['results'], guards):
                print >>f, failures, guard, data


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog logdir_or_file")

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(2)
    else:
        main(args[0])
