#!/usr/bin/python

# benchmarks-repo at 0d81c9b1ec8e

# for now: avg & stddev of the best

#    pypy-c-paper-jit bench.py -k5 raytrace/raytrace.py 1-4
#    pypy-c-paper-jit bench.py -k5 btree/btree.py 1-4
#    pypy-c-paper-jit bench.py -k5 skiplist/skiplist.py 1-4
#    pypy-c-paper-jit bench.py -k5 threadworms/threadworms.py 1-4
#    pypy-c-paper-jit bench.py -k5 mandelbrot/mandelbrot.py 1-4 64
#    pypy-c-paper-jit multithread-richards.py 10000 1-4 # report runtime



import matplotlib
import os
import sys
matplotlib.use('gtkagg')

from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

args = None
import matplotlib.pyplot as plt
# import pprint - slow as hell

# threads


interps_styles = {
    "pypy-stm-jit": {'fmt':'r-', 'linewidth':2},
    "pypy-jit": {'fmt':'g', 'dashes':(5, 2)},
    "jython": {'fmt':'m', 'dashes':(2, 5)},
    "best": {'fmt':"k:"}        # only fmt allowed
}

from collections import OrderedDict
benchs = OrderedDict([
    ("btree (large)", {
        "pypy-stm-jit":[
            [1.68,1.74,1.73,1.67,1.68,1.65],
            [1.35,1.54,1.52,1.28,1.31,1.28],
            [1.39,1.50,1.44,1.47,1.41,1.37],
            [1.66,1.67,1.68,1.66,1.71,1.71]
        ],
        "pypy-jit":[
            [1.61,1.62,1.61,1.59,1.59],
            [3.31,3.33,3.29,3.27,3.35],
            [5.11,5.20,5.07,5.00,5.25],
            [5.85,6.02,6.14,6.05,5.91]
        ]}),

    ("skiplist (large)", {
        "pypy-stm-jit":[
            [2.91,2.88,2.92,2.92,2.96],
            [3.05,2.90,2.89,2.93,2.94],
            [3.48,3.21,3.18,3.33,3.15],
            [3.87,3.69,3.78,3.81,3.66]
        ],
        "pypy-jit":[
            [2.14,2.17,2.31,2.24,2.34],
            [4.54,4.61,4.69,4.63,4.57],
            [6.29,6.14,6.25,6.16,6.21],
            [6.58,6.62,6.61,6.70,6.83]
        ]}),

    ("threadworms (large)", {
        "pypy-stm-jit":[
            [4.23,4.33,4.46,4.47,4.50],
            [3.4,3.34,3.39,3.32,3.02,3.13],
            [3.16,2.96,3.5,2.9,3.3],
            [3.4, 3.3,3.32,3.86,3.4]
        ],
        "pypy-jit":[
            [4.14,4.20,4.24,4.25,4.13],
            [12.5,11.4,12.3,11.9,11.7],
            [16.1,15.8,15.7,16.2,15.9],
            [20.3,19.8,18.9,19.7,19.5]
        ]}),

    ("mandelbrot (large)", {
        "pypy-stm-jit":[
            [17.87,17.88,17.88,17.63,17.75],
            [9.18,9.31,9.28,9.20,9.10,9.25],
            [7.75,7.8,7.81,7.7,7.09,7.59,7.43],
            [6.8,6.55,6.9,6.7,7.29,6.88,7.1]
        ],
        "pypy-jit":[
            [13.5,13.7,13.6,13.7,14.0],
            [14.3,14.6,14.6,14.1,14.4],
            [14.5,14.5,14.9,14.1,14.0],
            [14.1,14.6,14.9,14.1,14.2]
        ]}),

    ("raytrace (large)", {
        "pypy-stm-jit":[
            [3.91,3.87,3.88,3.92,3.98,3.95],
            [2.53,2.52,2.46,2.42,2.44,2.43],
            [2.23,2.17,2.12,2.16,2.30,2.35],
            [2.46,2.44,2.45,2.52,2.59,2.51]
        ],
        "pypy-jit":[
            [1.60,1.59,1.61,1.62,1.66,1.59],
            [3.02,3.01,3.15,3.21,2.91,3.19],
            [3.33,3.33,3.34,3.30,3.21,3.47],
            [3.57,3.67,3.34,3.48,3.46,3.61]
        ]}),

    ("richards (large)", {
        "pypy-stm-jit":[
            [63.4,61.3,62.4,71.2,63.9],
            [33.1,38.1,32.9,35.3,35.7],
            [24.9,36.1,24.9,33.4,25.4],
            [27.1,39.0,63.5,45.5,21.1]
        ],
        "pypy-jit":[
            [30.7,30.6,31.2,30.5,29.1],
            [31.4,28.5,31.5,29.7,32.8],
            [33.0,29.5,34.1,32.0,33.4],
            [32.0,32.4,34.6,32.6,31.4]
        ]})
])

def geom_mean(xs):
    return reduce(lambda x,y: x*y, xs, 1.0)**(1.0 / len(xs))

import numpy as np
sls = []
for bench_name, interps in benchs.items():
    slowdown = np.mean(interps["pypy-stm-jit"][0]) / np.mean(interps["pypy-jit"][0])
    print "overhead", bench_name, ":", slowdown
    sls.append(slowdown)


print "geom,max slowdown of STM", geom_mean(sls), np.max(sls)





def plot_speedups(plt, w, h, benchs, interps_styles):
    import numpy as np
    from collections import OrderedDict
    fig = plt.figure()

    ts = range(1,5) # threads
    legend = OrderedDict()
    axs = {}
    for i, (name, contestants) in enumerate(benchs.items()):
        if i >= w:
            sharex = axs[i - w]
        else:
            sharex = None
        ax = fig.add_subplot(h, w, i+1, sharex=sharex)
        axs[i] = ax
        max_y = 0
        best_y = 9999999
        for interp, runs in contestants.items():
            y = []
            yerr = []
            for r in runs:
                new_y = np.mean(r)
                y.append(new_y)
                yerr.append(np.std(r))
                if new_y > max_y:
                    max_y = new_y
                if new_y < best_y:
                    best_y = new_y

            artist = ax.errorbar(ts, y, yerr=yerr,
                                 **interps_styles[interp])
            if interp not in legend:
                legend[interp] = artist

        # legend["best"], = ax.plot(ts, [best_y] * len(ts),
        #                           interps_styles["best"]['fmt'])

        if i // w == h-1:
            ax.set_xlim(0, 5)
            ax.set_xlabel("Threads")
        ax.set_ylim(0, max_y * 1.1)
        if i % w == 0:
            ax.set_ylabel("Runtime [s]")
        ax.set_title(name)

    return axs[w*(h-1)].legend(tuple(legend.values()), tuple(legend.keys()),
                               ncol=4,
                               loc=(-0.15,-0.5))


def main():
    global fig

    print "Draw..."
    legend = plot_speedups(plt, 2, 3, benchs, interps_styles)

    #axs[0].set_ylim(0, len(x))
    #ax.set_yticks([r+0.5 for r in range(len(logs))])
    #ax.set_yticklabels(range(1, len(logs)+1))
    #axs[0].set_xticks([])

    # def label_format(x, pos):
    #     return "%.2f" % (abs((x - left) * 1e-6), )
    # major_formatter = matplotlib.ticker.FuncFormatter(label_format)
    # axs[0].xaxis.set_major_formatter(major_formatter)

    #ax.set_title("Memory Usage in Richards")

    plt.draw()
    #plt.show()
    print "Drawn."

    file_name = "performance.pdf"
    plt.savefig(file_name, format='pdf',
                bbox_extra_artists=(legend,),
                bbox_inches='tight', pad_inches=0)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Plot stm log files')
    parser.add_argument('--figure-size', default='7x8',
                        help='set figure size in inches: format=6x4')
    parser.add_argument('--font-size', default='10.0',
                        help='set font size in pts: 10.0')
    parser.add_argument('--png-dpi', default='300',
                        help='set dpi of png output: 300')


    args = parser.parse_args()
    matplotlib.rcParams.update(
        {'figure.figsize': tuple(map(int, args.figure_size.split('x'))),
         'font.size': float(args.font_size),
         'savefig.dpi': int(args.png_dpi),
         })


    main()
