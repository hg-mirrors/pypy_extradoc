#!/usr/bin/python

# benchmarks-repo at a26f2fb58413

# for now: avg & stddev of the best



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


#    pypy-c-paper-nojit bench.py -k5 raytrace/raytrace.py 1-4 256 256
#    pypy-c-paper-nojit bench.py -k5 btree/btree.py 1-4 500000
#    pypy-c-paper-nojit bench.py -k5 skiplist/skiplist.py 1-4 200000
#    pypy-c-paper-nojit bench.py -k5 threadworms/threadworms.py 1-4 500000
#    pypy-c-paper-nojit bench.py -k5 mandelbrot/mandelbrot.py 1-4 64 512 512
#    pypy-c-paper-nojit multithread-richards.py 30 1-4 # report runtime

benchs = {
    "raytrace (small)":{
        "pypy-stm-nojit":[
            [8.3, 8.04,7.99,7.91,8.03,],
            [4.33,4.21,4.28,4.23,4.24,],
            [3.74,3.61,3.09,4.18,3.01,],
            [3.08,2.89,2.75,3.06,2.98,]
        ],
        "cpython":[
            [2.5,2.55,2.51,2.54,2.52,],
            [2.7,2.67,2.67,2.69,2.71,],
            [2.75,2.77,2.75,2.80,2.76,],
            [2.84,2.83,2.85,2.86,2.83,]
        ],
        # "jython":[
        #     [2.95,2.95,2.96],
        #     [1.65,1.68,1.54],
        #     [1.2,1.15,1.3,1.3],
        #     [1.09,0.9,0.97,0.99,1.03]
        # ],
        "pypy-nojit":[
            [5.41,5.36,5.34,5.31,5.38],
            [6.66,6.63,6.61,6.51,6.60],
            [6.34,6.29,6.22,6.32,6.31],
            [5.91,5.72,5.88,5.87,5.78]
        ]},

    "btree (small)":{
        "pypy-stm-nojit":[
            [8.21,8.10,8.19,8.13,8.14],
            [4.60,4.64,4.61,5.21,4.65],
            [3.61,4.48,5.02,5.17,3.55],
            [4.01,4.07,4.68,4.07,3.76]
        ],
        "cpython":[
            [1.93,1.93,1.88,1.90,1.95],
            [5.76,5.78,5.78,5.71,5.79],
            [5.91,5.66,5.66,5.60,5.68],
            [6.03,5.98,6.01,6.03,5.97]
        ],
        # "jython":[
        #     [1.76,1.84],
        #     [2.60,2.46,2.6],
        #     [2.56,2.6,2.51],
        #     [2.57,2.52,2.48]
        # ],
        "pypy-nojit":[
            [6.23,6.41,6.27,6.23,6.29],
            [10.3,10.5,10.4,10.5,10.3],
            [11.4,11.4,11.3,11.3,11.5],
            [12.0,12.3,12.3,12.1,12.1]
        ]},

    "skiplist (small)":{
        "pypy-stm-nojit":[
            [5.80,5.91,6.10,5.71,5.58],
            [3.71,3.42,3.73,3.60,3.54],
            [3.22,2.95,3.25,3.61,3.03],
            [3.50,3.25,3.68,3.87,3.27]
        ],
        "cpython":[
            [3.3,3.1,3.3,3.2,3.3],
            [4.9,5.2,5.2,5.1,5.2],
            [5.0,5.4,5.3,5.3,5.4],
            [5.1,5.4,5.3,5.3,5.4]
        ],
        # "jython":[
        #     [1.38,1.33,1.47,1.40],
        #     [1.8,1.77,1.81],
        #     [1.81,1.79,1.88],
        #     [1.99,1.92,1.74,1.84]
        # ],
        "pypy-nojit":[
            [4.01,4.10,4.11,3.88,3.97],
            [5.92,5.84,5.74,6.16,5.76],
            [6.67,6.42,6.51,6.48,6.48],
            [6.50,6.59,6.93,6.61,6.56]
        ]},

    "threadworms (small)":{
        "pypy-stm-nojit":[
            [4.71,4.67,4.69,4.71,4.69],
            [2.61,2.55,2.53,2.52,2.56],
            [2.01,1.86,1.88,1.93,2.31],
            [2.14,2.02,2.46,2.06,1.69]
        ],
        "cpython":[
            [1.64,1.62,1.62,1.66,1.64],
            [5.08,5.10,5.08,5.01,5.16],
            [5.00,5.10,5.15,5.52,5.01],
            [5.37,5.30,5.41,5.21,5.10]
        ],
        # "jython":[
        #     [2.73,2.38,2.63,2.4],
        #     [3.0,2.87,3.3,3.1],
        #     [3.35,3.22,3.19],
        #     [3.19,3.37,3.26,3.36]
        # ],
        "pypy-nojit":[
            [4.02,4.03,4.01,4.05,4.05],
            [7.21,7.23,7.30,7.12,7.21],
            [8.05,8.03,8.08,8.12,8.02],
            [8.54,8.56,8.61,8.91,8.80]
        ]},

    "mandelbrot (small)":{
        "pypy-stm-nojit":[
            [5.35,5.30,5.23,5.15,5.21],
            [2.71,2.69,2.66,2.67,2.64],
            [1.96,1.81,1.87,1.83,1.91],
            [1.88,1.95,1.85,1.75,1.86]
        ],
        "cpython":[
            [1.65,1.70,1.61,1.73,1.66],
            [2.40,2.27,2.30,2.31,2.30],
            [2.41,2.46,2.34,2.42,2.46],
            [2.51,2.40,2.45,2.37,2.49]
        ],
        # "jython":[
        #     [5.56,5.61,5.59,5.55],
        #     [2.84,3,2.8,2.96],
        #     [2.13,2.03,2.04,2.11],
        #     [1.8,1.74,1.8,1.88]
        # ],
        "pypy-nojit":[
            [3.54,3.33,3.39,3.38,3.34],
            [4.43,4.43,4.47,4.47,4.46],
            [4.14,3.62,4.07,4.20,3.79],
            [3.88,3.83,3.82,3.79,3.88]
        ]},

    "richards (small)":{
        "pypy-stm-nojit":[
            [10.1,10.24,10.18,10.20,10.32],
            [5.71,5.79,5.73,5.75,5.75],
            [5.41,4.28,5.22,4.96,5.51],
            [4.61,4.62,4.51,4.49,5.08]
        ],
        "cpython":[
            [2.51,2.45,2.55,2.51,2.50],
            [3.87,3.71,3.88,3.81,3.75],
            [4.02,4.08,4.10,4.02,3.98],
            [4.13,4.01,4.15,3.99,4.12]
        ],
        # "jython":[
        #     [3.39,3.31,3.7],
        #     [2.32,1.95,2.18],
        #     [1.86,1.66],
        #     [1.49,1.63,1.59]
        # ],
        "pypy-nojit":[
            [5.95,6.02,5.99,5.92,6.03],
            [7.88,7.78,7.77,7.69,7.79],
            [7.01,7.02,7.17,7.05,7.21],
            [6.66,6.71,6.58,6.65,6.56]
        ]}
}

def geom_mean(xs):
    return reduce(lambda x,y: x*y, xs, 1.0)**(1.0 / len(xs))

import numpy as np
sls = []
spds = []
for bench_name, interps in benchs.items():
    slowdown = np.mean(interps["pypy-stm-nojit"][0]) / np.mean(interps["pypy-nojit"][0])
    speedup = np.mean(interps["pypy-stm-nojit"][0]) / np.mean(interps["pypy-stm-nojit"][3])
    print "overhead", bench_name, ":", slowdown
    print "stm speedup", bench_name, ":", speedup
    sls.append(slowdown)
    spds.append(speedup)


print "geom,max slowdown of STM", geom_mean(sls), np.max(sls)
print "geom,max speedup of STM", geom_mean(spds), np.max(spds)




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
