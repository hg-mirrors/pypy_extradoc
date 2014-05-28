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

# threads


interps_styles = {
    "pypy-stm-nojit": 'r-',
    "cpython": 'b--',
    "best": "k:"
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
        ]},

    "richards":{
        "pypy-stm-nojit":[
            [11.2],
            [6.1],
            [5.4,4.9],
            [4.8,4.9,5]
        ],
        "cpython":[
            [2.5],
            [3.87],
            [4.02],
            [4.13]
        ]}
}




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
