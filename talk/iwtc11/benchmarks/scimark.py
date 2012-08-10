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
    return "SOR(%d, %d)" % (n, cycles)

