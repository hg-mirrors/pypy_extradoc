#!/usr/bin/python

##########################################################
""" TODO: print thread-descriptor info on commit/abort """
##########################################################

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


ys = {10:[3.95, 7.99, 7.55, 5.39, 6.37, 7.46, 5.26],
      100:[7.16, 7.35, 8.82, 9.65, 7.91, 7.94, 7.56],
      1000:[9.81, 13.38, 14.25, 14.90, 13.26, 14.51, 14.69],
      10000:[8.83, 14.51, 14.35, 14.4, 11.96, 13.94, 14.94],
      100000:[8.23, 14.59, 14.48, 13.81, 13.64, 13.75, 13.72],
      1000000:[3.64, 4.63, 8.25, 3.63, 3.64, 6.46, 6.48],
      10000000:[3.55, 3.59, 3.55, 3.55, 3.56, 3.55, 3.55],
      }


def plot_tps(ax):
    import numpy as np
    x = []
    y = []
    yerr = []

    for k in sorted(ys.keys()):
        v = ys[k]
        x.append(k)
        y.append(np.mean(v))
        yerr.append(np.std(v))

    ax.errorbar(x, y, yerr=yerr)


def main():
    global fig

    print "Draw..."
    fig = plt.figure()

    ax = fig.add_subplot(111)

    plot_tps(ax)

    ax.set_xscale('log')
    ax.set_ylabel("Requests per Second (TPS)")
    ax.set_xlabel("reads\_limit")
    ax.set_xlim(5, 20000000)

    #axs[0].set_ylim(0, len(x))
    #ax.set_yticks([r+0.5 for r in range(len(logs))])
    #ax.set_yticklabels(range(1, len(logs)+1))
    #axs[0].set_xticks([])
    print "Drawn."

    # def label_format(x, pos):
    #     return "%.2f" % (abs((x - left) * 1e-6), )
    # major_formatter = matplotlib.ticker.FuncFormatter(label_format)
    # axs[0].xaxis.set_major_formatter(major_formatter)

    #legend = ax.legend()

    plt.draw()
    file_name = "setcheck.pdf"
    plt.savefig(file_name, format='pdf',
                # bbox_extra_artists=(legend,),
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
