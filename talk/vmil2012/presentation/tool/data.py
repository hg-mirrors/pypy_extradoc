from __future__ import division
import csv
import json
import os


COLORS = ["red", "green", "blue",
         "cyan", "magenta", "yellow",
         "black", "gray",  # "white",
         "darkgray", "lightgray", "brown",
         "lime", "olive", "orange",
         "pink", "purple", "teal",
         "violet"
        ]
def getlines(csvfile):
    with open(csvfile, 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        return [l for l in reader]


def we_are_n_percent(info, n):
    failure_counts = info['results'].values()
    failure_counts.sort()
    failure_counts.reverse()

    total_failures = sum(failure_counts)
    current_sum = 0
    for i, f in enumerate(failure_counts):
        current_sum += f
        if current_sum > total_failures * n / 100.0:
            return (i + 1)
    return -1


def build_plot_data(files):
    assert len(files) == 2
    with open(files[1]) as f:
        failures = json.load(f)
    for l in getlines(files[0]):
        failures[l['bench']]['nguards'] = float(l['number of guards'])

    output = []
    plot = """
\\addplot[%(color)s,mark=none] coordinates {
%(data)s
};
\\addplot[%(color)s,only marks,mark=*] coordinates {%(marks)s};
    """
    for j, (bench, info) in enumerate(failures.iteritems()):
        data = []
        marks = []
        color_map = {}
        results = info['results'].values()
        results.sort()
        results.reverse()

        num_50 = we_are_n_percent(info, 50)
        num_99 = we_are_n_percent(info, 99)
        num_99_dot_9 = we_are_n_percent(info, 99.9)

        marks.append("(%04f,%04f)" % (float(num_50) / (len(results) - 1), 
            float(results[num_50]) / max(results)))
        marks.append("(%04f,%04f)" % (float(num_99) / (len(results) - 1), 
            float(results[num_99]) / max(results)))
        marks.append("(%04f,%04f)" % (float(num_99_dot_9) / (len(results) - 1), 
            float(results[num_99_dot_9]) / max(results)))
        for i, result in enumerate(results):
            data.append("(%04f,%04f)" % (float(i) / (len(results) - 1),
                        float(result) / max(results)))
        #
        color_map[bench] = COLORS[j]
        if bench == 'go':
            with open('figures/go_data.tex', 'w') as f:
                f.write(plot % {'color': color_map[bench],
                                'name': bench,
                                'marks': " ".join(marks),
                                'data': " ".join(data)})
        output.append(plot % {'color': color_map[bench],
                              'name': bench,
                              'marks': " ".join(marks),
                              'data': " ".join(data)})

    with open('figures/data.tex', 'w') as f:
        for l in output:
            f.write(l)


def main():
    files = [os.path.realpath('../logs/'+ f) for f in ['resume_summary.csv',
        'guard_summary.json']]
    build_plot_data(files)


if __name__ == '__main__':
  main()
