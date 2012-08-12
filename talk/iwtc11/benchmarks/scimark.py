from convolution.convolution import Array2D
from array import array

def SOR_execute(omega, G, num_iterations):
    for p in xrange(num_iterations):
        for y in xrange(1, G.height - 1):
            for x in xrange(1, G.width - 1):
                G[x, y] = omega * 0.25 * (G[x, y-1] + G[x, y+1] + G[x-1, y] + G[x+1, y]) + \
                          (1.0 - omega) * G[x, y]
def SOR(args):
    n, cycles = map(int, args)
    a = Array2D(n, n)
    SOR_execute(1.25, a, cycles)
    return "SOR(%d, %d)" % (n, cycles)


def SparseCompRow_matmult(M, y, val, row, col, x, num_iterations):
    for reps in xrange(num_iterations):
        for r in xrange(M):
            sa = 0.0
            for i in xrange(row[r], row[r+1]):
                sa += x[ col[i] ] * val[i]
            y[r] = sa

def SparseMatMult(args):
    N, nz, cycles = map(int, args)
    x = array('d', [0]) * N
    y = array('d', [0]) * N
    result = 0.0
    nr = nz / N
    anz = nr * N
    val = array('d', [0]) * anz
    col = array('i', [0]) * nz
    row = array('i', [0]) * (N + 1)
    row[0] = 0
    for r in xrange(N):
        rowr = row[r]
        step = r / nr
        row[r+1] = rowr + nr
        if (step < 1):
            step = 1
        for i in xrange(nr):
            col[rowr + i] = i * step
    SparseCompRow_matmult(N, y, val, row, col, x, cycles);
    return "SparseMatMult(%d, %d, %d)" % (N, nz, cycles)


