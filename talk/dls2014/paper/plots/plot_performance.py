#!/usr/bin/python

# benchmarks-repo at 0d81c9b1ec8e

# for now: avg & stddev of the best

#    pypy-c-paper-jit bench.py -k7 raytrace/raytrace.py 1-4
#    pypy-c-paper-jit bench.py -k7 btree/btree.py 1-4
#    pypy-c-paper-jit bench.py -k7 skiplist/skiplist.py 1-4
#    pypy-c-paper-jit bench.py -k7 threadworms/threadworms.py 1-4
#    pypy-c-paper-jit bench.py -k7 mandelbrot/mandelbrot.py 1-4 64
#    pypy-c-paper-jit multithread-richards.py 3000 1-4 # report runtime
# miller_rabin: pypy-c-paper-jit bench.py -k7 primes/primes.py 1-4
# mersenne: pypy-c-paper-jit bench.py -k7 mersenne/mersenne.py 1-4


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
            [1.67845606804,1.65006303787,1.66974020004,1.63858819008,1.66356801987],
            [1.33803701401,1.32292485237,1.31796693802,1.35001111031,1.31932878494],
            [1.36447811127,1.36002612114,1.36561393738,1.33688187599,1.36755800247],
            [1.57205200195,1.57919001579,1.56078600883,1.5807390213,1.53369808197],
        ],
        "pypy-jit":[
            [1.55986404419,1.56078219414,1.55183196068,1.56036901474,1.55763506889],
            [3.08302307129,3.07977199554,3.19185519218,3.08162689209,3.15804696083],
            [4.98545002937,5.04515981674,5.00658583641,5.05858302116,5.0690600872],
            [5.81887507439,5.83665108681,5.82539606094,5.85461807251,5.80481886864],
        ]}),

    ("skiplist (large)", {
        "pypy-stm-jit":[
            [2.8317830562591553, 2.9466500282287598, 2.777143955230713, 2.9067370891571045, 2.868476152420044],
            [2.9228100776672363, 2.9347541332244873, 2.9178760051727295, 2.9834980964660645, 2.957442045211792],
            [3.15556001663208, 3.139164924621582, 3.1457889080047607, 3.2395389080047607, 3.176427125930786],
            [3.60280704498291, 3.591495990753174, 3.5838911533355713, 3.6133289337158203, 3.5673019886016846],
        ],
        "pypy-jit":[
            [2.1221060752868652, 2.1250720024108887, 2.1107590198516846, 2.131819009780884, 2.1142380237579346],
            [4.392746210098267, 4.336360216140747, 4.410413980484009, 4.3028059005737305, 4.448081970214844],
            [6.0925071239471436, 6.012751817703247, 5.994383811950684, 5.925648927688599, 6.02409815788269],
            [6.677470922470093, 6.746111154556274, 6.772925138473511, 6.698845148086548, 6.861325025558472],
        ]}),

    ("threadworms (large)", {
        "pypy-stm-jit":[
            [4.517525911331177, 4.548923015594482, 4.584195137023926, 4.576831102371216, 4.5510969161987305],
            [3.2610208988189697, 3.287199020385742, 3.2835729122161865, 2.83652400970459, 3.355794906616211],
            [2.552337169647217, 3.3851380348205566, 3.3292200565338135, 2.512721061706543, 3.395833969116211],
            [3.0494518280029297, 3.304857015609741, 3.465865135192871, 3.483139991760254, 2.9930028915405273],
        ],
        "pypy-jit":[
            [4.137892007827759, 4.017345190048218, 4.04946494102478, 4.033931016921997, 4.049654006958008],
            [12.235527038574219, 12.323483943939209, 12.391777992248535, 12.369697093963623, 12.642794132232666],
            [16.1,15.8,15.7,16.2,15.9],
            [20.3,19.8,18.9,19.7,19.5]
        ]}),

    ("miller-rabin (large)", {
        "pypy-stm-jit":[
            [2.469092845916748, 2.465752124786377, 2.5735549926757812, 2.424694061279297, 2.4528331756591797],
            [1.6964740753173828, 1.7057690620422363, 1.687267780303955, 1.6836810111999512, 1.7357711791992188],
            [1.9504740238189697, 1.9206480979919434, 1.959285020828247, 1.9674179553985596, 1.9120190143585205],
            [2.1957740783691406, 2.259826898574829, 2.246433973312378, 2.158545970916748, 2.1627681255340576],
        ],
        "pypy-jit":[
            [2.161806106567383, 2.1457087993621826, 2.144040107727051, 2.151695966720581, 2.1421849727630615],
            [3.4412081241607666, 3.4092049598693848, 3.4685871601104736, 3.388669013977051, 3.453207015991211],
            [4.572340965270996, 4.519361972808838, 4.503000020980835, 4.507853984832764, 4.442840814590454],
            [5.5019919872283936, 5.51775598526001, 5.487698078155518, 5.485651969909668, 5.482367038726807],
        ]}),

    ("mandelbrot (large)", {
        "pypy-stm-jit":[
            [17.430854082107544, 17.26646614074707, 17.176318883895874, 17.15704083442688, 17.212379217147827],
            [9.08885383605957, 9.0710289478302, 9.040630102157593, 9.0260329246521, 9.00651502609253],
            [6.48170804977417, 6.4656219482421875, 6.51883602142334, 6.484840154647827, 6.444514036178589],
            [5.4356160163879395, 5.4222729206085205, 5.4224090576171875, 5.452478885650635, 5.4159040451049805],
        ],
        "pypy-jit":[
            [13.5,13.7,13.6,13.7,14.0],
            [14.3,14.6,14.6,14.1,14.4],
            [14.5,14.5,14.9,14.1,14.0],
            [14.1,14.6,14.9,14.1,14.2]
        ]}),

    ("raytrace (large)", {
        "pypy-stm-jit":[
            [3.9185469150543213, 3.8989100456237793, 3.8274168968200684, 3.844446897506714, 3.8334569931030273],
            [2.2376699447631836, 2.236940860748291, 2.1736011505126953, 2.1718149185180664, 2.1718950271606445],
            [1.8365809917449951, 1.83445405960083, 1.8318328857421875, 1.830247163772583, 1.8350648880004883],
            [1.7387700080871582, 1.7485370635986328, 1.7356500625610352, 1.7735240459442139, 1.7386369705200195],
        ],
        "pypy-jit":[
            [1.5851430892944336, 1.5589039325714111, 1.5606789588928223, 1.5591561794281006, 1.5676798820495605],
            [2.041408061981201, 2.042022943496704, 2.018625020980835, 2.0331828594207764, 1.9610838890075684],
            [3.759972095489502, 3.7670998573303223, 3.787578821182251, 3.7681820392608643, 3.75722599029541],
            [4.019146919250488, 4.016950845718384, 4.092247009277344, 4.044332981109619, 4.066432952880859],
        ]}),

    ("richards (large)", {
        "pypy-stm-jit":[
            [17.73,17.73,17.74,17.72,17.73],
            [10.41,10.43,10.43,10.39,10.41],
            [9.73,9.77,9.81,9.74,9.67],
            [9.95,10.00,9.95,10.00,9.94],
        ],
        "pypy-jit":[
            [8.87,8.89,8.89,8.87,8.90],
            [9.79,9.79,9.81,9.75,9.80],
            [9.95,9.95,9.95,9.98,9.93],
            [9.04,9.06,9.01,9.11,9.21]
        ]}),

    ("mersenne (large)", {
        "pypy-stm-jit":[
            [9.245907068252563, 9.243618965148926, 9.244323968887329, 9.241997957229614, 9.242669820785522],
            [4.897014141082764, 4.882230043411255, 4.881627082824707, 4.883110046386719, 4.883028030395508],
            [3.603656053543091, 3.6193759441375732, 3.6500911712646484, 3.613867998123169, 3.607400894165039],
            [3.6181468963623047, 3.716840982437134, 3.6233408451080322, 3.7763969898223877, 3.4737911224365234],

        ],
        "pypy-jit":[
            [5.46359395980835, 5.463193893432617, 5.461122035980225, 5.4631431102752686, 5.46463680267334],
            [5.476777076721191, 5.47367787361145, 5.4741599559783936, 5.473356008529663, 5.47412896156311],
            [5.497221946716309, 5.484626054763794, 5.478212833404541, 5.484951972961426, 5.490041017532349],
            [5.511621952056885, 5.505235910415649, 5.497171878814697, 5.482274055480957, 5.495197772979736],
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
    legend = plot_speedups(plt, 2, 4, benchs, interps_styles)

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
    parser.add_argument('--figure-size', default='7x10',
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
