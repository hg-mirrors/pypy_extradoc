import sys
from collections import defaultdict

word_to_kib = 1024 / 8. # 64 bit
numberings_per_word = 2/8. # two bytes

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

    kib_snapshots = results['num_snapshots'] * 4. / word_to_kib # gc, jitcode, pc, prev
    naive_kib_snapshots = results['naive_num_snapshots'] * 4. / word_to_kib
    kib_numbering = results['size_estimate_numbering'] / word_to_kib
    naive_kib_numbering = results['naive_size_estimate_numbering'] / word_to_kib
    kib_consts = results['num_consts'] * 4 / word_to_kib
    naive_kib_consts = results['naive_num_consts'] * 4 / word_to_kib
    kib_virtuals = results['size_virtuals'] / word_to_kib
    naive_kib_virtuals = results['naive_size_virtuals'] / word_to_kib
    kib_setfields = results['size_setfields'] / word_to_kib
    print "storages:", results['num_storages']
    print "snapshots: %sKiB vs %sKiB" % (kib_snapshots, naive_kib_snapshots)
    print "numberings: %sKiB vs %sKiB" % (kib_numbering, naive_kib_numbering)
    print "optimal: %s" % (results['optimal_numbering'] / word_to_kib)
    print "consts:  %sKiB vs %sKiB" % (kib_consts, naive_kib_consts)
    print "virtuals:  %sKiB vs %sKiB" % (kib_virtuals, naive_kib_virtuals)
    print "number virtuals: %i vs %i" % (results['num_virtuals'], results['naive_num_virtuals'])
    print "setfields: %sKiB" % (kib_setfields, )
    print "--"
    print "total:  %sKiB vs %sKiB" % (      kib_snapshots +       kib_numbering +       kib_consts +       kib_virtuals + kib_setfields,
                                      naive_kib_snapshots + naive_kib_numbering + naive_kib_consts + naive_kib_virtuals + kib_setfields)


if __name__ == '__main__':
    main(sys.argv)
