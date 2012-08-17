import sys
import time

def count_mult_of_5(N):
    mult = 0
    not_mult = 0
    for i in range(N):
        if i % 5 == 0:
            mult += 1
        else:
            not_mult += 1
    return mult, not_mult

def main():
    N = int(sys.argv[1])
    start = time.clock()
    count = count_mult_of_5(N)
    end = time.clock()
    print 'count: ', count
    print 'time:', end-start, 'secs'

if __name__ == '__main__':
    main()
