#!/usr/bin/python

# benchmarks-repo at 0d81c9b1ec8e

# for now: avg & stddev of the best

#    pypy-c-paper-nojit bench.py -k5 raytrace/raytrace.py 1-4 256 256
#    pypy-c-paper-nojit bench.py -k5 btree/btree.py 1-4 500000
#    pypy-c-paper-nojit bench.py -k5 skiplist/skiplist.py 1-4 200000
#    pypy-c-paper-nojit bench.py -k5 threadworms/threadworms.py 1-4 500000
#    pypy-c-paper-nojit bench.py -k5 mandelbrot/mandelbrot.py 1-4 64 512 512
#    pypy-c-paper-nojit multithread-richards.py 30 1-4 # report runtime


from plot_performance import plot_speedups
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


interps_styles = {
    "pypy-stm-nojit": {'fmt':'r-', 'linewidth':2},
    "cpython": {'fmt':'b', 'dashes':(1,1)},
    "pypy-nojit": {'fmt':'g', 'dashes':(5, 2)},
    "jython": {'fmt':'m', 'dashes':(2, 5)},
    "best": {'fmt':"k:"}        # only fmt allowed
}



benchs = {
    "raytrace":{
        "pypy-stm-nojit":[
            [8.3],
            [4.33],
            [3.74],
            [3.08]
        ],
        "cpython":[
            [2.5],
            [2.7],
            [2.75],
            [2.84]
        ],
        "jython":[
            [2.95,2.95,2.96],
            [1.65,1.68,1.54],
            [1.2,1.15,1.3,1.3],
            [1.09,0.9,0.97,0.99,1.03]
        ],
        "pypy-nojit":[
            [5.5,5.7,5.8],
            [7,6.97],
            [6.68,6.77],
            [6.4,6.4]
        ]},

    "btree":{
        "pypy-stm-nojit":[
            [8.3],
            [4.9],
            [3.9,4.3],
            [4.4,4.0,4.3]
        ],
        "cpython":[
            [1.93],
            [5.76],
            [5.91],
            [6.03]
        ],
        "jython":[
            [1.76,1.84],
            [2.60,2.46,2.6],
            [2.56,2.6,2.51],
            [2.57,2.52,2.48]
        ],
        "pypy-nojit":[
            [6.63,6.73],
            [10.6,10.5],
            [11.4,11.4],
            [12.0,12.3]
        ]},

    "skiplist":{
        "pypy-stm-nojit":[
            [5.8],
            [3.9],
            [3.22,4.2,3.5],
            [3.5,3.44,4.3]
        ],
        "cpython":[
            [3.3],
            [4.9],
            [5.0],
            [5.1]
        ],
        "jython":[
            [1.38,1.33,1.47,1.40],
            [1.8,1.77,1.81],
            [1.81,1.79,1.88],
            [1.99,1.92,1.74,1.84]
        ],
        "pypy-nojit":[
            [4.9,4.8,4.6,4.7],
            [6.87,7.53,6.64],
            [7.74,7.3,7.35],
            [7.38,7.28,7.31,7.54]
        ]},

    "threadworms":{
        "pypy-stm-nojit":[
            [4.8],
            [2.7],
            [2.0,2.2,2.1],
            [2.1,2.3,2.2]
        ],
        "cpython":[
            [1.64],
            [5],
            [5.2],
            [5.37]
        ],
        "jython":[
            [2.73,2.38,2.63,2.4],
            [3.0,2.87,3.3,3.1],
            [3.35,3.22,3.19],
            [3.19,3.37,3.26,3.36]
        ],
        "pypy-nojit":[
            [4.49,4.36],
            [7.86,7.81],
            [8.76,8.73],
            [9.23,9.27]
        ]},

    "mandelbrot":{
        "pypy-stm-nojit":[
            [5.35],
            [2.8],
            [1.96,2.2],
            [2.33,1.97]
        ],
        "cpython":[
            [1.65],
            [2.4],
            [2.4],
            [2.5]
        ],
        "jython":[
            [5.56,5.61,5.59,5.55],
            [2.84,3,2.8,2.96],
            [2.13,2.03,2.04,2.11],
            [1.8,1.74,1.8,1.88]
        ],
        "pypy-nojit":[
            [3.67,3.54],
            [4.53,4.82,4.75],
            [4.14,4.23],
            [4.38,4.23]
        ]},

    "richards":{
        "pypy-stm-nojit":[
            [10.7],
            [6.1],
            [5.4,4.9],
            [4.8,4.9,5]
        ],
        "cpython":[
            [2.5],
            [3.87],
            [4.02],
            [4.13]
        ],
        "jython":[
            [3.39,3.31,3.7],
            [2.32,1.95,2.18],
            [1.86,1.66],
            [1.49,1.63,1.59]
        ],
        "pypy-nojit":[
            [6.6,6.5],
            [7.98,7.98],
            [7.56,7.33],
            [7.05,7.28]
        ]}
}

import numpy as np
sls = []
for bench_name, interps in benchs.items():
    slowdown = np.mean(interps["pypy-stm-nojit"][0]) / np.mean(interps["pypy-nojit"][0])
    print "overhead", bench_name, ":", slowdown
    sls.append(slowdown)
print "avg,max slowdown of STM", np.mean(sls), np.max(sls)




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

    file_name = "performance_nojit.pdf"
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
