import csv
import os
import sys
import tempfile
from collections import defaultdict

from backenddata import collect_logfiles
from pypy.tool import logparser

word_to_kib = 1024 / 8. # 64 bit
numberings_per_word = 2/8. # two bytes

def compute_compressed_length(data):
    import subprocess
    cmd = "xz -9 --stdout -"
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    compressed, _ = process.communicate(data)
    return len(compressed) / 1024.


def cond_incr(d, key, obj, seen, incr=1):
    if obj not in seen:
        seen.add(obj)
        d[key] += incr
    d["naive_" + key] += incr

def compute_numbers(infile):
    seen = set()
    seen_numbering = set()
    # all in words
    results = defaultdict(float)
    log = logparser.parse_log_file(infile)
    rdata = logparser.extract_category(log, 'jit-resume')
    results["num_guards"] = len(rdata)
    # compute compressed size
    all_data = "\n".join(rdata)
    results["strlength"] = len(all_data)
    results["compressedlength"] = compute_compressed_length(all_data)
    # compute resume data size estimates
    for log in rdata:
        for line in log.splitlines():
            if line.startswith("Log storage"):
                results['num_storages'] += 1
                continue
            if not line.startswith("\t"):
                continue
            line = line[1:]
            if line.startswith("jitcode/pc"):
                _, address = line.split(" at ")
                cond_incr(results, "num_snapshots", address, seen)
            elif line.startswith("numb"):
                content, address = line.split(" at ")
                size =  line.count("(") * numberings_per_word + 3 # gc, len, prev
                cond_incr(results, "optimal_numbering", content, seen_numbering, size)
                cond_incr(results, "size_estimate_numbering", address, seen, size)
            elif line.startswith("const "):
                address, _ = line[len("const "):].split("/")
                cond_incr(results, "num_consts", address, seen)
            elif "info" in line:
                _, address = line.split(" at  ")
                if line.startswith("varrayinfo"):
                    factor = numberings_per_word
                elif line.startswith("virtualinfo") or line.startswith("vstructinfo") or line.startswith("varraystructinfo"):
                    factor = 1 + numberings_per_word # one descr reference per entry
                naive_factor = factor
                if address in seen:
                    factor = 0
                else:
                    results['num_virtuals'] += 1
                    results['size_virtuals'] += 1 # an entry in the list of virtuals
                results['naive_num_virtuals'] += 1
                results['naive_size_virtuals'] += 1 # an entry in the list of virtuals
                target = "size_virtuals"
                naive_target = "naive_size_virtuals"

                cond_incr(results, "size_virtuals", address, seen, 4) # bit of a guess
            elif "pending setfields" == line.strip():
                results['size_setfields'] += 3 # reference to object, gc, len
                factor = 3 # descr, index, numbering from, numbering to (plus alignment)
                naive_factor = 0
                target = "size_setfields"
                naive_target = "naive_size_setfields" # dummy
            elif line[0] == "\t":
                results[target] += factor
                results[naive_target] += naive_factor

    results["kib_snapshots"] = results['num_snapshots'] * 4. / word_to_kib # gc, jitcode, pc, prev
    results["naive_kib_snapshots"] = results['naive_num_snapshots'] * 4. / word_to_kib
    results["kib_numbering"] = results['size_estimate_numbering'] / word_to_kib
    results["naive_kib_numbering"] = results['naive_size_estimate_numbering'] / word_to_kib
    results["kib_consts"] = results['num_consts'] * 4 / word_to_kib
    results["naive_kib_consts"] = results['naive_num_consts'] * 4 / word_to_kib
    results["kib_virtuals"] = results['size_virtuals'] / word_to_kib
    results["naive_kib_virtuals"] = results['naive_size_virtuals'] / word_to_kib
    results["kib_setfields"] = results['size_setfields'] / word_to_kib
    results["total"] = (
        results[      "kib_snapshots"] +
        results[      "kib_numbering"] +
        results[      "kib_consts"] +
        results[      "kib_virtuals"] +
        results[      "kib_setfields"])
    results["naive_total"] = (
        results["naive_kib_snapshots"] +
        results["naive_kib_numbering"] +
        results["naive_kib_consts"] +
        results["naive_kib_virtuals"] +
        results["naive_kib_setfields"])
    return results


def main(argv):
    import optparse
    parser = optparse.OptionParser(usage="%prog logdir_or_file")

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(2)
        return
    path = args[0]
    if os.path.isdir(path):
        dirname = path
    else:
        dirname = os.path.dirname(path)
    files = collect_logfiles(path)
    with file("logs/resume_summary.csv", "w") as f:
        csv_writer = csv.writer(f)
        row = ["exe", "bench", "number of guards", "total resume data size", "naive resume data size"]
        csv_writer.writerow(row)

        for exe, bench, infile in files:
            results = compute_numbers(os.path.join(dirname, infile))
            row = [exe, bench, results["num_guards"], results['total'], results['naive_total'], results['compressedlength']]
            csv_writer.writerow(row)

            print "=============================="
            print bench
            print "storages:", results['num_storages']
            print "snapshots: %sKiB vs %sKiB" % (results["kib_snapshots"], results["naive_kib_snapshots"])
            print "numberings: %sKiB vs %sKiB" % (results["kib_numbering"], results["naive_kib_numbering"])
            print "optimal: %s" % (results['optimal_numbering'] / word_to_kib)
            print "consts:  %sKiB vs %sKiB" % (results["kib_consts"], results["naive_kib_consts"])
            print "virtuals:  %sKiB vs %sKiB" % (results["kib_virtuals"], results["naive_kib_virtuals"])
            print "number virtuals: %i vs %i" % (results['num_virtuals'], results['naive_num_virtuals'])
            print "setfields: %sKiB" % (results["kib_setfields"], )
            print "--"
            print "total:  %sKiB vs %sKiB vs %sKiB" % (results["total"], results["naive_total"], results['compressedlength'])


if __name__ == '__main__':
    main(sys.argv)
