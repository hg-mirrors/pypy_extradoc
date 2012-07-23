import sys
from collections import defaultdict

word_to_kib = 1024 / 4.

def cond_incr(d, key, obj, seen, incr=1):
    if obj not in seen:
        seen.add(obj)
        d[key] += incr
    d["naive_" + key] += incr

def main(argv):
    infile = argv[1]
    seen = set()
    seen_numbering = set()
    # all in words
    results = defaultdict(float)
    size_estimate_virtuals = 0
    naive_consts = 0
    with file(infile) as f:
        for line in f:
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
                size =  line.count("(") / 2.0 + 3 # gc, len, prev
                cond_incr(results, "optimal_numbering", content, seen_numbering, size)
                cond_incr(results, "size_estimate_numbering", address, seen, size)
            elif line.startswith("const "):
                address, _ = line[len("const "):].split("/")
                cond_incr(results, "num_consts", address, seen)
    kib_snapshots = results['num_snapshots'] * 4. / word_to_kib # gc, jitcode, pc, prev
    naive_kib_snapshots = results['naive_num_snapshots'] * 4. / word_to_kib
    kib_numbering = results['size_estimate_numbering'] / word_to_kib
    naive_kib_numbering = results['naive_size_estimate_numbering'] / word_to_kib
    kib_consts = results['num_consts'] * 4 / word_to_kib
    naive_kib_consts = results['naive_num_consts'] * 4 / word_to_kib
    print "storages:", results['num_storages']
    print "snapshots: %sKiB vs %sKiB" % (kib_snapshots, naive_kib_snapshots)
    print "numberings: %sKiB vs %sKiB" % (kib_numbering, naive_kib_numbering)
    print "optimal: %s" % (results['optimal_numbering'] / word_to_kib)
    print "consts:  %sKiB vs %sKiB" % (kib_consts, naive_kib_consts)
    print "--"
    print "total:  %sKiB vs %sKiB" % (kib_snapshots+kib_numbering+kib_consts,
                                      naive_kib_snapshots+naive_kib_numbering+naive_kib_consts)


if __name__ == '__main__':
    main(sys.argv)
