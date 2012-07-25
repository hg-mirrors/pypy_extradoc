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


def build_ops_count_table(csvfile, texfile, template):
    lines = getlines(csvfile)

    head = ['Benchmark',
            'ops b/o',
            '\\% guards b/o',
            'ops a/o',
            '\\% guards a/o',
            'opt. rate',
            'guard opt. rate']

    table = []
    # collect data
    for bench in lines:
        keys = 'numeric guard set get rest new'.split()
        ops_bo = sum(int(bench['%s before' % s]) for s in keys)
        ops_ao = sum(int(bench['%s after' % s]) for s in keys)
        guards_bo = int(bench['guard before'])
        guards_ao = int(bench['guard after'])
        res = [
                bench['bench'].replace('_', '\\_'),
                ops_bo,
                "%.2f (%s)" % (guards_bo / ops_bo * 100,
                                 bench['guard before']),
                ops_ao,
                "%.2f (%s)" % (guards_ao / ops_ao * 100,
                                  bench['guard after']),
                "%.2f" % ((1 - ops_ao / ops_bo) * 100,),
                "%.2f" % ((1 - guards_ao / guards_bo) * 100,),
              ]
        table.append(res)
    output = render_table(template, head, sorted(table))
    write_table(output, texfile)


def build_backend_count_table(csvfile, texfile, template):
    lines = getlines(csvfile)

    head = ['Benchmark',
            'Machine code size (kB)',
            'll resume data (kB)']

    table = []
    # collect data
    for bench in lines:
        bench['bench'] = bench['bench'].replace('_', '\\_')
        keys = ['bench', 'asm size', 'guard map size']
        table.append([bench[k] for k in keys])
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
            ('summary.csv', build_ops_count_table),
        'backend_table.tex':
            ('backend_summary.csv', build_backend_count_table)
        }


def main(table):
    tablename = os.path.basename(table)
    if tablename not in tables:
        raise AssertionError('unsupported table')
    data, builder = tables[tablename]
    csvfile = os.path.join('logs', data)
    texfile = os.path.join('figures', tablename)
    template = os.path.join('tool', 'table_template.tex')
    builder(csvfile, texfile, template)


if __name__ == '__main__':
    assert len(sys.argv) > 1
    main(sys.argv[1])
