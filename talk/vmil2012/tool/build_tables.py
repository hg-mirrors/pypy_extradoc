from __future__ import division
import csv
import django
from django.template import Template, Context
import os
import sys

# This line is required for Django configuration
django.conf.settings.configure()


def getlines(csvfile):
    with open(csvfile, 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        return [l for l in reader]


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

        res = [bench['bench'].replace('_', '\\_'),]
        for t in ('before', 'after'):
            values = []
            for key in keys:
                o = int(bench['%s %s' % (key, t)])
                values.append(o / ops[t] * 100)

            assert 100.0 - sum(values) < 0.0001
            res.extend(['%.2f ' % v for v in values])
        table.append(res)
    output = render_table(template, head, sorted(table))
    write_table(output, texfile)



def build_benchmarks_table(csvfiles, texfile, template):
    assert len(csvfiles) == 2
    lines = getlines(csvfiles[0])
    bridge_lines = getlines(csvfiles[1])
    bridgedata = {}
    for l in bridge_lines:
        bridgedata[l['bench']] = l

    head = ['Benchmark',
            'ops b/o',
            '\\% guards b/o',
            'ops a/o',
            '\\% guards a/o',
            'opt. rate in \\%',
            'guard opt. rate in \\%',
            'bridges']

    table = []
    # collect data
    keys = 'numeric guard set get rest new'.split()
    for bench in lines:
        ops_bo = sum(int(bench['%s before' % s]) for s in keys)
        ops_ao = sum(int(bench['%s after' % s]) for s in keys)
        guards_bo = int(bench['guard before'])
        guards_ao = int(bench['guard after'])
        # the guard count collected from jit-summary counts more guards than
        # actually emitted, so the number collected from parsing the logfiles
        # will probably be lower
        assert guards_ao <= bridgedata[bench['bench']]['guards']
        res = [
                bench['bench'].replace('_', '\\_'),
                ops_bo,
                "%.2f" % (guards_bo / ops_bo * 100,),
                ops_ao,
                "%.2f" % (guards_ao / ops_ao * 100,),
                "%.2f" % ((1 - ops_ao / ops_bo) * 100,),
                "%.2f" % ((1 - guards_ao / guards_bo) * 100,),
                bridgedata[bench['bench']]['bridges'],
              ]
        table.append(res)
    output = render_table(template, head, sorted(table))
    write_table(output, texfile)


def build_backend_count_table(csvfiles, texfile, template):
    lines = getlines(csvfiles[0])
    resume_lines = getlines(csvfiles[1])
    resumedata = {}
    for l in resume_lines:
        resumedata[l['bench']] = l

    head = ['Benchmark',
            'Machine code size (kB)',
            'hl resume data (kB)',
            'll resume data (kB)',
            'machine code resume data relation in \\%']

    table = []
    # collect data
    for bench in lines:
        name = bench['bench']
        bench['bench'] = bench['bench'].replace('_', '\\_')
        gmsize = float(bench['guard map size'])
        asmsize = float(bench['asm size'])
        rdsize = float(resumedata[name]['total resume data size'])
        rel = "%.2f" % (asmsize / (gmsize + rdsize) * 100,)
        table.append([
            bench['bench'],
            "%.2f" % (asmsize,),
            "%.2f" % (rdsize,),
            "%.2f" % (gmsize,),
            rel])
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
            (['backend_summary.csv', 'resume_summary.csv'], build_backend_count_table),
        'ops_count_table.tex':
            (['summary.csv'], build_ops_count_table),
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
