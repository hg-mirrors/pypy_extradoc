from __future__ import division
import csv
import django
import json
import os
import sys
from django.template import Template, Context

# This line is required for Django configuration
django.conf.settings.configure()


def getlines(csvfile):
    with open(csvfile, 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        return [l for l in reader]


def build_failing_guards_table(files, texfile, template):
    BRIDGE_THRESHOLD = 200
    assert len(files) == 2
    with open(files[1]) as f:
        failures = json.load(f)
    for l in getlines(files[0]):
        failures[l['bench']]['nguards'] = float(l['number of guards'])

    table = []
    head = ['Benchmark',
            'Sparkline' + "~" * 8,
            'Failing',
            '> %d failures' % BRIDGE_THRESHOLD,
            '50\% of failures',
            '99\% of failures',
            '99.9\% of failures',
            ]
    mins = [(10000, 0)] * (len(head) - 2)
    maxs = [(0, 0)] * (len(head) - 2)
    for i, (bench, info) in enumerate(failures.iteritems()):
        total = info['nguards']
        total_failures = len(info['results'])
        bridges = len([k for k, v in info['results'].iteritems()
                                            if v > BRIDGE_THRESHOLD])
        perc_failures = (100 * total_failures / total)
        perc_bridges = (100 * bridges / total)
        num_50 = we_are_n_percent(info, 50)
        num_99 = we_are_n_percent(info, 99)
        num_99_dot_9 = we_are_n_percent(info, 99.9)
        perc_50 = num_50 / total * 100
        perc_99 = num_99 / total * 100
        perc_99_dot_9 = num_99_dot_9 / total * 100

        mins[0] = min(mins[0], (perc_failures, i))
        maxs[0] = max(maxs[0], (perc_failures, i))

        mins[1] = min(mins[1], (perc_bridges, i))
        maxs[1] = max(maxs[1], (perc_bridges, i))

        mins[2] = min(mins[2], (perc_50, i))
        maxs[2] = max(maxs[2], (perc_50, i))

        mins[3] = min(mins[3], (perc_99, i))
        maxs[3] = max(maxs[3], (perc_99, i))

        mins[4] = min(mins[4], (perc_99_dot_9, i))
        maxs[4] = max(maxs[4], (perc_99_dot_9, i))

        res = [bench.replace('_', '\\_'),
                make_sparkline(info['results'], num_50 - 1,
                                num_99 - 1, num_99_dot_9 - 1),
                "%.1f\\%%" % perc_failures,
                "%.1f\\%%" % perc_bridges,
                "%d~~\\textasciitilde{}~~%.3f\\%%" %
                                    (num_50, perc_50),
                "%d~~\\textasciitilde{}~~%.3f\\%%" %
                                    (num_99, perc_99),
                "%d~~\\textasciitilde{}~~%.3f\\%%" %
                                    (num_99_dot_9, perc_99_dot_9),
        ]
        table.append(res)
    mark_min_max(table, mins, maxs, 2)
    output = render_table(template, head, sorted(table))
    write_table(output, texfile)


def mark_min_max(table, mins, maxs, offs):
    # mark minima
    for column, (_, index) in enumerate(mins):
        table[index][column + offs] = "\cellcolor{darkgray}%s" % \
                                    table[index][column + offs]

    # mark maxima
    for column, (_, index) in enumerate(maxs):
        table[index][column + offs] = "\cellcolor{lightgray}%s" % \
                                    table[index][column + offs]


def we_are_n_percent(info, n):
    failure_counts = info['results'].values()
    print failure_counts
    failure_counts.sort()
    print failure_counts
    failure_counts.reverse()
    print failure_counts

    total_failures = sum(failure_counts)
    current_sum = 0
    for i, f in enumerate(failure_counts):
        current_sum += f
        if current_sum > total_failures * n / 100.0:
            return (i + 1)
    return -1


def make_sparkline(results, index_50, index_99, index_99_9):
    results = results.values()
    results.sort()
    results.reverse()
    lines = ["\\begin{sparkline}{20}"]
    lines.append("\\sparkdot %04f %04f blue" %
            (float(index_50) / (len(results) - 1),
                float(results[index_50]) / max(results)))
    lines.append("\\sparkdot %04f %04f red" %
            (float(index_99) / (len(results) - 1),
                float(results[index_99]) / max(results)))
    lines.append("\\sparkdot %04f %04f green" %
            (float(index_99_9) / (len(results) - 1),
                float(results[index_99_9]) / max(results)))
    lines.append("\\spark")
    for i, result in enumerate(results):
        lines.append("%04f %04f" %
                (float(i) / (len(results) - 1),
                    float(result) / max(results)))
    lines.append("/")
    lines.append("\\end{sparkline}")
    return " ".join(lines)


def build_resume_data_table(csvfiles, texfile, template):
    assert len(csvfiles) == 1
    lines = getlines(csvfiles[0])
    table = []
    head = ['Benchmark', 'Compressed', 'Naive', 'xz compressed']
    mins = [(99999, 0)] * 3
    maxs = [(0, 0)] * 3
    for i, bench in enumerate(lines):
        total = float(bench['total resume data size'])
        naive = float(bench['naive resume data size'])
        xz = float(bench['compressed resume data size'])
        mins[0] = min(mins[0], (total, i))
        maxs[0] = max(maxs[0], (total, i))

        mins[1] = min(mins[1], (naive, i))
        maxs[1] = max(maxs[1], (naive, i))

        mins[2] = min(mins[2], (xz, i))
        maxs[2] = max(maxs[2], (xz, i))
        res = [bench['bench'].replace('_', '\\_'),
                "%.2f {\scriptsize KiB}" % (total,),  # (100*total/naive)),
                "%.2f {\scriptsize KiB}" % (naive),  # , 100*naive/total),
                "%.2f {\scriptsize KiB}" % (xz),  # , 100*xz/total),
        ]
        table.append(res)
    # mark min
    mark_min_max(table, mins, maxs, 1)
    output = render_table(template, head, sorted(table))
    write_table(output, texfile)


def build_ops_count_table(csvfiles, texfile, template):
    assert len(csvfiles) == 1
    lines = getlines(csvfiles[0])
    keys = 'numeric set get rest new guard '.split()
    table = []
    head = ['Benchmark']
    head += ['%s b' % k for k in keys]
    head += ['%s a' % k for k in keys]

    for bench in lines:
        ops = {'before': sum(int(bench['%s before' % s]) for s in keys),
                'after': sum(int(bench['%s after' % s]) for s in keys)}

        res = [bench['bench'].replace('_', '\\_')]
        for t in ('before', 'after'):
            values = []
            for key in keys:
                o = int(bench['%s %s' % (key, t)])
                values.append(o / ops[t] * 100)

            assert 100.0 - sum(values) < 0.0001
            res.extend(['%.1f\\%%' % v for v in values])
        table.append(res)
    output = render_table(template, head, sorted(table))
    write_table(output, texfile)


def build_guard_table(csvfiles, texfile, template):
    assert len(csvfiles) == 1
    lines = getlines(csvfiles[0])
    table = []
    head = ['Benchmark', 'Guards before', 'Guards after']

    keys = 'numeric set get rest new guard '.split()
    for bench in lines:
        ops = {'before': sum(int(bench['%s before' % s]) for s in keys),
                'after': sum(int(bench['%s after' % s]) for s in keys)}

        res = [bench['bench'].replace('_', '\\_')]
        for t in ('before', 'after'):
            o = int(bench['guard %s' % t])
            res.append('%.1f\\%%' % (o / ops[t] * 100))
        table.append(res)
    output = render_table(template, head, sorted(table))
    write_table(output, texfile)


def build_benchmarks_table(csvfiles, texfile, template):
    assert len(csvfiles) == 2
    lines = getlines(csvfiles[0])
    bridge_lines = getlines(csvfiles[1])
    # keep this around for the assertion bellow
    bridgedata = {}
    for l in bridge_lines:
        bridgedata[l['bench']] = l

    head = ['Benchmark',
            '\# Traces',
            'Ops. before',
            'Guards before',
            'Ops. after',
            'Guards after',
            'Opt. rate',
            'Guard opt. rate',
            ]
    mins = [(99999, 0)] * (len(head) - 1)
    maxs = [(0, 0)] * (len(head) - 1)

    table = []
    # collect data
    keys = 'numeric guard set get rest new'.split()
    for i, bench in enumerate(lines):
        ops_bo = sum(int(bench['%s before' % s]) for s in keys)
        ops_ao = sum(int(bench['%s after' % s]) for s in keys)
        guards_bo = int(bench['guard before'])
        perc_guards_bo = guards_bo / ops_bo * 100
        guards_ao = int(bench['guard after'])
        perc_guards_ao = guards_ao / ops_ao * 100
        opt_rate = (1 - ops_ao / ops_bo) * 100
        guard_opt_rate = (1 - guards_ao / guards_bo) * 100
        no_traces = bench['number of loops'] + bridgedata[bench['bench']]['bridges']

        mins[0] = min(mins[0], (no_traces, i))
        maxs[0] = max(maxs[0], (no_traces, i))

        mins[1] = min(mins[1], (ops_bo, i))
        maxs[1] = max(maxs[1], (ops_bo, i))

        mins[2] = min(mins[2], (perc_guards_bo, i))
        maxs[2] = max(maxs[2], (perc_guards_bo, i))

        mins[3] = min(mins[3], (ops_ao, i))
        maxs[3] = max(maxs[3], (ops_ao, i))

        mins[4] = min(mins[4], (perc_guards_ao, i))
        maxs[4] = max(maxs[4], (perc_guards_ao, i))

        mins[5] = min(mins[5], (opt_rate, i))
        maxs[5] = max(maxs[5], (opt_rate, i))

        mins[6] = min(mins[6], (guard_opt_rate, i))
        maxs[6] = max(maxs[6], (guard_opt_rate, i))
        # the guard count collected from jit-summary counts more guards than
        # actually emitted, so the number collected from parsing the logfiles
        # will probably be lower
        assert guards_ao <= bridgedata[bench['bench']]['guards']
        res = [
                bench['bench'].replace('_', '\\_'),
                no_traces,
                ops_bo,
                "%d~~\\textasciitilde{}~~%.1f\\%%" %
                                        (guards_bo, perc_guards_bo),
                ops_ao,
                "%d~~\\textasciitilde{}~~%.1f\\%%" %
                                        (guards_ao, perc_guards_ao),
                "%.1f\\%%" % (opt_rate,),
                "%.1f\\%%" % (guard_opt_rate,),
              ]
        table.append(res)
    mark_min_max(table, mins, maxs, 1)
    output = render_table(template, head, sorted(table))
    write_table(output, texfile)


def build_backend_count_table(csvfiles, texfile, template):
    lines = getlines(csvfiles[0])
    resume_lines = getlines(csvfiles[1])
    resumedata = {}
    for l in resume_lines:
        resumedata[l['bench']] = l

    head = [r'Benchmark',
            r'Code',
            r'Resume data',
            r'Backend map',
            #r'Relation',
            ]
    mins = [(99999, 0)] * (len(head) - 1)
    maxs = [(0, 0)] * (len(head) - 1)

    table = []
    # collect data
    for i, bench in enumerate(lines):
        name = bench['bench']
        bench['bench'] = bench['bench'].replace('_', '\\_')
        gmsize = float(bench['guard map size'])
        asmsize = float(bench['asm size'])
        rdsize = float(resumedata[name]['total resume data size'])
        mins[0] = min(mins[0], (asmsize, i))
        maxs[0] = max(maxs[0], (asmsize, i))

        mins[1] = min(mins[1], (rdsize, i))
        maxs[1] = max(maxs[1], (rdsize, i))

        mins[2] = min(mins[2], (gmsize, i))
        maxs[2] = max(maxs[2], (gmsize, i))
        table.append([
            r"%s" % bench['bench'],
            r"%.1f {\scriptsize KiB}" % (asmsize,),
            r"%.1f {\scriptsize KiB}" % (rdsize,),
            r"%.1f {\scriptsize KiB}" % (gmsize,),
            #rel,
            ])
    mark_min_max(table, mins, maxs, 1)
    output = render_table(template, head, sorted(table))
    write_table(output, texfile)


def write_table(output, texfile):
    # Write the output to a file
    with open(texfile, 'w') as out_f:
        out_f.write(output)


def render_table(ttempl, head, table):
    # open and read template
    with open(ttempl) as f:
        t = Template(f.read())
    c = Context({"head": head, "table": table})
    return t.render(c)


tables = {
        'benchmarks_table.tex':
            (['summary.csv', 'bridge_summary.csv'], build_benchmarks_table),
        'backend_table.tex':
            (['backend_summary.csv', 'resume_summary.csv'],
                                    build_backend_count_table),
        'ops_count_table.tex':
            (['summary.csv'], build_ops_count_table),
        'guard_table.tex':
            (['summary.csv'], build_guard_table),
        'resume_data_table.tex':
            (['resume_summary.csv'], build_resume_data_table),
        'failing_guards_table.tex':
            (['resume_summary.csv', 'guard_summary.json'],
                                    build_failing_guards_table),
        }


def main(table):
    tablename = os.path.basename(table)
    if tablename not in tables:
        raise AssertionError('unsupported table')
    data, builder = tables[tablename]
    csvfiles = [os.path.join('logs', d) for d in data]
    texfile = os.path.join('figures', tablename)
    template = os.path.join('tool', 'table_template.tex')
    builder(csvfiles, texfile, template)


if __name__ == '__main__':
    assert len(sys.argv) > 1
    main(sys.argv[1])
