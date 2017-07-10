import numpy as np
import matplotlib.pyplot as plt

N = 5
CPYTHON = (4.99, 2.85, 1.62, 0.59)
PYPY = (288.67, 278.25, 276.81, 235.91)

def draw(title, values, allvalues, color):
    filename = '%s-v%d.png' % (title, len(values)-1)
    ylim = max(allvalues) * 1.20
    labels = ['v%d' % i for i in range(len(values))]
    extra = len(allvalues) - len(values)
    values = values + (0,)*extra
    labels = labels + ['']*extra
    
    ind = np.arange(len(values))
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    ax.bar(ind, values, width, color=color)
    ax.set_ylabel('fps')
    ax.set_title(title + ' FPS')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(labels)
    ax.set_ylim((0, ylim))
    print filename
    plt.savefig(filename)

for i in range(1, len(CPYTHON)+1):
    draw('PyPy', PYPY[:i], PYPY, color='r')
    draw('CPython', CPYTHON[:i], CPYTHON, color='b')


## for i, (cpy, pypy) in enumerate(zip(CPYTHON, PYPY)):
##     print i, pypy/cpy
