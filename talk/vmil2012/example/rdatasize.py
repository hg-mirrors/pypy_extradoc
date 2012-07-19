import sys

word_to_kib = 1024 / 4.

def main(argv):
    infile = argv[1]
    seen = set()
    seen_numbering = set()
    # all in words
    num_storages = 0
    num_snapshots = 0
    naive_num_snapshots = 0
    size_estimate_numbering = 0
    naive_estimate_numbering = 0
    optimal_numbering = 0
    size_estimate_virtuals = 0
    num_consts = 0
    naive_consts = 0
    with file(infile) as f:
        for line in f:
            if line.startswith("Log storage"):
                num_storages += 1
                continue
            if not line.startswith("\t"):
                continue
            line = line[1:]
            if line.startswith("jitcode/pc"):
                _, address = line.split(" at ")
                if address not in seen:
                    seen.add(address)
                    num_snapshots += 1 # gc, jitcode, pc, prev
                naive_num_snapshots += 1
            elif line.startswith("numb"):
                content, address = line.split(" at ")
                size =  line.count("(") / 2.0 + 3 # gc, len, prev
                if content not in seen_numbering:
                    seen_numbering.add(content)
                    optimal_numbering += size
                if address not in seen:
                    seen.add(address)
                    size_estimate_numbering += size
                naive_estimate_numbering += size
            elif line.startswith("const "):
                address, _ = line[len("const "):].split("/")
                if address not in seen:
                    seen.add(address)
                    num_consts += 1
                naive_consts += 1
    kib_snapshots = num_snapshots * 4. / word_to_kib
    naive_kib_snapshots = naive_num_snapshots * 4. / word_to_kib
    kib_numbering = size_estimate_numbering / word_to_kib
    naive_kib_numbering = naive_estimate_numbering / word_to_kib
    kib_consts = num_consts * 4 / word_to_kib
    naive_kib_consts = naive_consts * 4 / word_to_kib
    print "storages:", num_storages
    print "snapshots: %sKiB vs %sKiB" % (kib_snapshots, naive_kib_snapshots)
    print "numberings: %sKiB vs %sKiB" % (kib_numbering, naive_kib_numbering)
    print "optimal: %s" % (optimal_numbering / word_to_kib)
    print "consts:  %sKiB vs %sKiB" % (kib_consts, naive_kib_consts)
    print "--"
    print "total:  %sKiB vs %sKiB" % (kib_snapshots+kib_numbering+kib_consts,
                                      naive_kib_snapshots+naive_kib_numbering+naive_kib_consts)


if __name__ == '__main__':
    main(sys.argv)
