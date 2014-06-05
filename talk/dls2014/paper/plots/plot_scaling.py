#!/usr/bin/python

# obtained with time on
#   pypy-c --jit off bench_scaling.py [1-4]


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

xs = range(1,5)
ys = [[1.78,1.79,1.75,1.81,1.76],
      [1.82,1.82,1.80,1.80,1.8],
      [1.88,1.97,1.89,1.90,1.94],
      [1.96,1.99,1.87,2.00,1.97,2.09,1.98,2.12]]



def plot_mems(ax):
    import numpy as np
    y = []
    yerr = []
    # opt_y = [1.0] * len(xs)
    first_time = np.mean(ys[0])
    for x, d in zip(xs, ys):
        normalized = map(lambda x:x/first_time, d)
        y.append(np.mean(normalized))
        yerr.append(np.std(normalized))

    print y
    ax.errorbar(xs, y, yerr=yerr,
                label="pypy-stm-nojit")
    # ax.plot(xs, opt_y, label="optimal")
    return ax.legend(loc=4)


def main():
    global fig

    print "Draw..."
    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.set_ylabel("Runtime normalized to 1 thread")
    ax.set_xlabel("Threads")
    ax.set_ylim(0, 1.3)
    ax.set_xlim(0, 5)

    legend = plot_mems(ax)


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

    file_name = "scaling.pdf"
    plt.savefig(file_name, format='pdf',
                bbox_extra_artists=(legend,),
                bbox_inches='tight', pad_inches=0)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Plot stm log files')
    parser.add_argument('--figure-size', default='6x3',
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
