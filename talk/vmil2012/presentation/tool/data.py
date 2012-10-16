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
    print failure_counts
    failure_counts.sort()
    print failure_counts
    failure_counts.reverse()
    print failure_counts

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
\\addplot[%(color)s] coordinates {
%(data)s
};
    """
    for j, (bench, info) in enumerate(failures.iteritems()):
        data = []
        results = info['results'].values()
        results.sort()
        results.reverse()
        for i, result in enumerate(results):
            data.append("(%04f,%04f)" % (float(i) / (len(results) - 1),
                        float(result) / max(results)))

        if bench == 'go':
            with open('figures/go_data.tex', 'w') as f:
                f.write(plot % {'color': 'black', 'name': bench, 'data': " ".join(data)})
        output.append(plot % {'color':COLORS[j], 'name': bench, 'data': " ".join(data)})

    with open('figures/data.tex', 'w') as f:
        for l in output:
            f.write(l)


def main():
    files = [os.path.realpath('../logs/'+ f) for f in ['resume_summary.csv',
        'guard_summary.json']]
    build_plot_data(files)


if __name__ == '__main__':
  main()
