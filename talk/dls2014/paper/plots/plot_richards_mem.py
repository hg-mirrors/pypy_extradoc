#!/usr/bin/python

# obtained log-file with
#   pypy-c --jit off ~/pypy/benchmarks/multithread/multithread-richards.py 60 4 2>richards_mem.log
# rss using measure_memusage.sh



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

with open('richards_mem.log') as f:
    xs = []
    y1s = []
    y2s = []
    first_time = None
    for line in f.readlines():
        line = line.strip().strip("{").strip("}")
        time, mems = line.split(":")
        if not first_time:
            first_time = float(time)
        xs.append(float(time) - first_time)
        real_mem, max_rss, page_util = mems.split("/")
        y1s.append(int(real_mem) / 1024. / 1024)
        y2s.append(float(page_util))

# RSS:
# x2s = range(12)
# y2s = [152304, 180060, 180428,
#        180448, 180460, 180696,
#        180124, 180552, 180584,
#        180588, 180544, 180252]
# y2s = map(lambda x: x / 1024., y2s)


def plot_mems(ax, ax2):
    print sum(y1s) / len(xs)
    print sum(y2s) / len(xs)
    a, = ax.plot(xs, y1s, 'b-o', ms=3)
    b, = ax2.plot(xs, y2s, 'r-x', ms=3)
    return ax.legend((a, b),
                     ('GC managed memory', 'Page privatisation'))


def main():
    global fig

    print "Draw..."
    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.set_ylabel("Memory [MiB]", color='b')
    ax.set_xlabel("Runtime [s]")
    ax.set_ylim(0, 50)

    ax2 = ax.twinx()
    ax.set_xlim(-0.5, 9.8)
    ax2.set_ylim(0, 1.5)
    ax2.set_ylabel("Ratio = ${private~pages}\over{shared~pages}$",
                   color='r')
    legend = plot_mems(ax, ax2)


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

    file_name = "richards_mem.pdf"
    plt.savefig(file_name, format='pdf',
                bbox_extra_artists=(legend,),
                bbox_inches='tight', pad_inches=0)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Plot stm log files')
    parser.add_argument('--figure-size', default='6x4',
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
