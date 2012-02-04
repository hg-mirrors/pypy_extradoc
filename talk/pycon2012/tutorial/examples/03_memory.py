
import time, os, re, gc

class A(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

def read_smaps():
    with open("/proc/%d/smaps" % os.getpid()) as f:
        mark = False
        for line in f:
            if mark:
                assert line.startswith('Size:')
                m = re.search('(\d+).*', line)
                return m.group(0), int(m.group(1))
            if 'heap' in line:
                mark = True

def main():
    l = []
    count = 0
    for k in range(100):
        t0 = time.time()
        for i in range(100000):
            l.append(A(1, 2, i))
            for j in range(4):
                A(1, 1, 2)
        count += i
        print time.time() - t0
        usage, kb = read_smaps()
        print usage, kb * 1024 / count, "per instance"
        gc.collect()
        usage, kb = read_smaps()
        print "after collect", usage, kb * 1024 / count, "per instance"
        #import pdb
        #pdb.set_trace()
        time.sleep(1)

if __name__ == '__main__':
    main()
