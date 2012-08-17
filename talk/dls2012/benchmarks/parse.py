
import pdb, sys

NAME_REPL = {
    'dilate3x3(Array2D(1000x1000))': 'dilate3x3(1000,1000)',
    'sobel_magnitude(1000,1000)': 'sobel(1000,1000)',
    'conv3(array(1e5))': 'conv3(1e5)',
    'conv3(array(1e6))': 'conv3(1e6)',
    'conv5(array(1e5))': 'conv5(1e5)',
    'conv5(array(1e6))': 'conv5(1e6)',
    'sobel(Array2D(1000x1000))': 'sobel(1000,1000)',
    'sobel(Array(1000x1000))': 'sobel(1000,1000)',
    'conv3x3(Array2D(1000000x3))': 'conv3x3(1000000,3)',
    'conv3x3(Array2D(1000x1000))': 'conv3x3(1000,1000)',
    'dilate3x3(1000)': 'dilate3x3(1000,1000)',
    'conv3x3(1000)': 'conv3x3(1000,1000)',
    'conv3x3(3)': 'conv3x3(1000000,3)',
}

def main(name):
    interp = None
    res = {}
    order = ['python2.7', 'pypy --jit enable_opts=intbounds:rewrite:virtualize:string:earlyforce:pure:heap:ffi', 'pypy', 'luajit -O-loop', 'luajit', 'gcc -O3 -march=native -fno-tree-vectorize']
    with open(name) as f:
        for line in f:
            line = line.strip("\n")
            if not line:
                interp = None
            elif interp is None:
                interp = line
            else:
                bench, rest = line.split(':')
                bench = bench.replace(" ", "")
                bench = NAME_REPL.get(bench, bench)
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
                    # to get a 95% confidence interval, the std deviation is multiplied with a factor
                    # see the table at http://en.wikipedia.org/wiki/Standard_deviation#Rules_for_normally_distributed_data
                    sys.stdout.write(' & %.2f $\pm$ %.3f' % (e[0], e[1] * 1.959964))
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
