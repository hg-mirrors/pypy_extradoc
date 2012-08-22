
import pdb, sys
import numpy as np
import matplotlib.pyplot as plt

# force type 1 fonts
import matplotlib

matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True

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
    'SparseMatMult(1000,5000,262144)': 'SparseMatMult(1e4,5e3,262144)',
    'SparseMatMult(100000,1000000,1024)': 'SparseMatMult(1e5,1e6,1024)',
}

IGNORE = {
    "conv3(1e5)",
    "conv5(1e5)",
    "conv5(1e6)",
    "conv3x3(1000000,3)",
}

def main(name):
    interp = None
    res = {}
    order = ['python2.7', 'pypy --jit enable_opts=intbounds:rewrite:virtualize:string:earlyforce:pure:heap:ffi', 'pypy', 'luajit -O-loop', 'luajit', 'gcc -O3 -march=native -fno-tree-vectorize']
    labels = [None, 'PyPy no LP', 'PyPy', 'LuaJIT no LP', 'LuaJIT', None]
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
                if bench in IGNORE:
                    continue
                if '+-' in rest:
                    a, d = rest.split('+-')
                    res.setdefault(bench, {})[interp] = float(a), float(d)
                else:
                    res.setdefault(bench, {})[interp] = float(rest)
    resmat = np.zeros((len(res), len(order)))
    benchmarks = res.keys()
    benchmarks.sort()
    assert benchmarks[-3] == "sqrt(Fix16)"
    del benchmarks[-3]
    benchmarks.append("sqrt(Fix16)")
    for i, key in enumerate(benchmarks):
        sys.stdout.write(key)
        for j, ord in enumerate(order):
            try:
                e = res[key][ord]
            except KeyError:
                sys.stdout.write(" & -")
            else:
                if isinstance(e, tuple):
                    # to get a 95% confidence interval, the std deviation is multiplied with a factor
                    # see the table at http://en.wikipedia.org/wiki/Standard_deviation#Rules_for_normally_distributed_data
                    sys.stdout.write(' & %.2f $\pm$ %.3f' % (e[0], e[1] * 1.959964))
                    resmat[i, j] = e[0]
                else:
                    sys.stdout.write(' & %.2f' % e)
                    resmat[i, j] = e
        sys.stdout.write('\\\\\n')
        print "\hline"

    width = 0.8 / sum(1 for l in labels if l)
    x = np.array(range(len(res))[::-1])
    plt.figure(figsize=(10, 15))
    #plt.subplot(111).set_xscale("log")
    r = plt.plot([1, 1], [0, len(res)+0.5], 'k--')
    legend = ([r[0]], ['gcc -O3'])
    max_factor = 10
    for i, l  in enumerate(labels):
        if not l:
            continue
        bottoms = x + (len(labels) - 1 - i) * width + 0.3/2
        print bottoms
        result = resmat[:,i]/resmat[:,-1]
        for k, entry in enumerate(result):
            if entry > max_factor:
                print bottoms[k], 1
                plt.text(max_factor, bottoms[k], " %.1fx" % entry)
                result[k] = max_factor
        r = plt.barh(bottoms, result, width,
                     color=str(1. / (len(labels) - 1) * i))
        legend[0].append(r[0])
        legend[1].append(l)
    plt.yticks(x + 0.5 + width, benchmarks)
    plt.subplots_adjust(left=0.35, right=0.93, top=0.99, bottom=0.02)
    plt.legend(*legend, loc=4)
    plt.ylim((0, len(res)+0.5))
    #plt.show()
    plt.savefig('result.pdf')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: parse.py <input file>"
    try:
        main(sys.argv[1])
    except:
        pdb.post_mortem(sys.exc_info()[2])
