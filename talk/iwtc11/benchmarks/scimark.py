from convolution.convolution import Array2D
from array import array

class Random(object):
    MDIG = 32
    ONE = 1
    m1 = (ONE << (MDIG-2)) + ((ONE << (MDIG-2) )-ONE)
    m2 = ONE << MDIG/2
    dm1  = 1.0 / float(m1);

    def __init__(self, seed):
        self.initialize(seed)
        self.left = 0.0
        self.right = 1.0
        self.width = 1.0
        self.haveRange = False

    def initialize(self, seed):
    
        self.seed = seed
        seed = abs(seed)
        jseed = min(seed, self.m1)
        if (jseed % 2 == 0):
            jseed -= 1
        k0 = 9069 % self.m2;
        k1 = 9069 / self.m2;
        j0 = jseed % self.m2;
        j1 = jseed / self.m2;
        self.m = array('d', [0]) * 17 
        for iloop in xrange(17):
            jseed = j0 * k0;
            j1 = (jseed / self.m2 + j0 * k1 + j1 * k0) % (self.m2 / 2);
            j0 = jseed % self.m2;
            self.m[iloop] = j0 + self.m2 * j1;
        self.i = 4;
        self.j = 16;

    def nextDouble(self):
        I, J, m = self.i, self.j, self.m
        k = m[I] - m[J];
        if (k < 0):
            k += self.m1;
        self.m[J] = k;

        if (I == 0):
            I = 16;
        else:
            I -= 1;
        self.i = I;

        if (J == 0):
            J = 16;
        else:
            J -= 1;
        self.j = J;

        if (self.haveRange):
            return  self.left +  self.dm1 * float(k) * self.width;
        else:
            return self.dm1 * float(k);



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


