
import pdb, sys

def main(name):
    interp = None
    res = {}
    order = ['python2.7', 'python2.6 psyco-wrapper.py', 'pypy --jit enable_opts=intbounds:rewrite:virtualize:heap', 'pypy', 'gcc -O2', 'gcc -O3 -march=native -fno-tree-vectorize']
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
    try:
        main('new_result.txt')
    except:
        pdb.post_mortem(sys.exc_info()[2])
