from convolution.convolution import Array2D

def SOR_execute(omega, G, num_iterations):
    for p in xrange(num_iterations):
        for i in xrange(1, G.height - 1):
            for j in xrange(1, G.width - 1):
                G[j, i] = omega * 0.25 * (G[j, i-1] + G[j, i+1] + G[j-1, i] +
                                          G[j+1, i] + (1.0 - omega) * G[j, i])
def SOR(args):
    n, cycles = map(int, args)
    a = Array2D(n, n)
    SOR_execute(1.25, a, cycles)

if __name__ == '__main__':
    from time import time
    for i in range(10):
        t0 = time()
        #SOR([100, 32768]) # gcc -O3: 2.51, pypy-1.8: 3.83
        SOR([1000, 256]) # gcc -O3 2.07, pypy-1.8: 3.03
        t1 = time()
        print t1-t0
