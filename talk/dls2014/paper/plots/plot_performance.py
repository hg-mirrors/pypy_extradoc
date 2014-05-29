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
    "pypy-jit": {'fmt':'b', 'dashes':(1,1)},
    "jython": {'fmt':'m', 'dashes':(2, 5)},
    "best": {'fmt':"k:"}        # only fmt allowed
}

benchs = {
    "raytrace":{
        "pypy-stm-jit":[
            [3.91, 3.87],
            [2.53, 2.52],
            [2.23],
            [2.46, 2.6,2.76,2.51]
        ],
        "pypy-jit":[
            [1.6],
            [2.17],
            [3.33],
            [4.16]
        ]},

    "btree":{
        "pypy-stm-jit":[
            [1.68],
            [1.3],
            [1.39],
            [1.66,1.67,1.68,1.66]
        ],
        "pypy-jit":[
            [1.6],
            [3.3],
            [5.1],
            [5.8]
        ]},

    "skiplist":{
        "pypy-stm-jit":[
            [2.9],
            [3.0],
            [3.4],
            [3.8]
        ],
        "pypy-jit":[
            [2.14],
            [4.5],
            [6.2],
            [6.58]
        ]},

    "threadworms":{
        "pypy-stm-jit":[
            [4.23,4.33],
            [3.4,3.34,3.39],
            [3.16,2.96,3.5,2.9,3.3],
            [3.4, 3.3,3.32,3.86]
        ],
        "pypy-jit":[
            [4.14],
            [12.5],
            [16],
            [20]
        ]},

    "mandelbrot":{
        "pypy-stm-jit":[
            [17.87,17.88,17.88],
            [9.4,9.42,9.34],
            [7.75,7.8,8.2,7.7],
            [6.8,6.55,6.9,6.7]
        ],
        "pypy-jit":[
            [13.5],
            [14.3],
            [14.5],
            [14.1]
        ]},

    "richards":{
        "pypy-stm-jit":[
            [63.4],
            [33.1],
            [24.9,36],
            [27,39,63]
        ],
        "pypy-jit":[
            [30.7],
            [31.4],
            [33],
            [32.0]
        ]}
}




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
