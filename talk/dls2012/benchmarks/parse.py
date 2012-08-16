
import pdb, sys

def main(name):
    interp = None
    res = {}
    order = ['python2.7', 'pypy --jit enable_opts=intbounds:rewrite:virtualize:string:earlyforce:pure:heap:ffi', 'pypy', 'gcc -O3 -march=native -fno-tree-vectorize', 'luajit', 'luajit -O-loop']
    with open(name) as f:
        for line in f:
            line = line.strip("\n")
            if not line:
                interp = None
            elif interp is None:
                interp = line
            else:
                bench, rest = line.split(':')
                if '+-' in rest:
                    a, d = rest.split('+-')
                    res.setdefault(bench, {})[interp] = float(a), float(d)
                else:
                    res.setdefault(bench, {})[interp] = float(rest)
    for key in sorted(res.keys()):
        sys.stdout.write(key)
        for ord in order:
            try:
                e = res[key][ord]
            except KeyError:
                sys.stdout.write(" & -")
            else:
                if isinstance(e, tuple):
                    sys.stdout.write(' & %.2f +- %.2f' % (e[0], e[1]))
                else:
                    sys.stdout.write(' & %.2f' % e)
        sys.stdout.write('\\\\\n')
        print "\hline"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: parse.py <input file>"
    try:
        main(sys.argv[1])
    except:
        pdb.post_mortem(sys.exc_info()[2])
