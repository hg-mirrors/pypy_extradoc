def plot_benchmarks(filename, *pythons):
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.rcParams['figure.figsize'] = (20,15)

    data = {"CPython": {"simple.noargs": 0.43, "simple.onearg(None)": 0.45, "simple.onearg(i)": 0.44, "simple.varargs": 0.6, "simple.allocate_int": 0.46, "simple.allocate_tuple": 0.81, "obj.noargs": 0.44, "obj.onearg(None)": 0.48, "obj.onearg(i)": 0.47, "obj.varargs": 0.63, "len(obj)": 0.34, "obj[0]": 0.25},
            "PyPy 5.8": {"simple.noargs": 1.09, "simple.onearg(None)": 1.34, "simple.onearg(i)": 2.6, "simple.varargs": 2.74, "simple.allocate_int": 2.49, "simple.allocate_tuple": 8.21, "obj.noargs": 1.27, "obj.onearg(None)": 1.55, "obj.onearg(i)": 2.85, "obj.varargs": 3.06, "len(obj)": 1.36, "obj[0]": 1.53},
            "PyPy 5.9": {"simple.noargs": 0.16, "simple.onearg(None)": 0.2, "simple.onearg(i)": 1.61, "simple.varargs": 3.08, "simple.allocate_int": 1.69, "simple.allocate_tuple": 6.39, "obj.noargs": 1.17, "obj.onearg(None)": 1.74, "obj.onearg(i)": 3.03, "obj.varargs": 2.95, "len(obj)": 1.24, "obj[0]": 1.37},
            "PyPy 5.10": {"simple.noargs": 0.18, "simple.onearg(None)": 0.21, "simple.onearg(i)": 1.52, "simple.varargs": 2.59, "simple.allocate_int": 1.67, "simple.allocate_tuple": 6.44, "obj.noargs": 1.12, "obj.onearg(None)": 1.41, "obj.onearg(i)": 2.62, "obj.varargs": 2.89, "len(obj)": 1.21, "obj[0]": 1.32},
            "PyPy 6.0": {"simple.noargs": 0.18, "simple.onearg(None)": 0.2, "simple.onearg(i)": 0.22, "simple.varargs": 0.42, "simple.allocate_int": 0.89, "simple.allocate_tuple": 5.02, "obj.noargs": 0.19, "obj.onearg(None)": 0.22, "obj.onearg(i)": 0.24, "obj.varargs": 0.45, "len(obj)": 0.15, "obj[0]": 0.28}}



    #pythons = data.keys()
    #pythons = ["CPython", "PyPy 5.10", "PyPy 6.0"]
    benchmarks = sorted(data[pythons[0]].keys())

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(len(benchmarks))
    bar_width = 0.20
    opacity = 0.8

    colors = ('blue', 'orange', 'red') #'bgryk'

    for i, python in enumerate(pythons):
        values = [data[python][bench] for bench in benchmarks]
        normalized = [v/data['CPython'][bench] for (v, bench) in zip(values, benchmarks)]
        #print python, values
        rects1 = plt.bar(index + bar_width*i, normalized, bar_width,
                         label=python,
                         color=colors[i])

    plt.xlabel('Benchmark')
    plt.ylabel('Time (normalized)')
    plt.title('cpyext microbenchmarks')
    plt.xticks(index + bar_width, benchmarks, rotation=45)
    plt.legend()

    plt.savefig(filename)

plot_benchmarks("pypy58.png", "CPython", "PyPy 5.8")
plot_benchmarks("pypy60.png", "CPython", "PyPy 5.8", "PyPy 6.0")
