from scimark import SOR_execute, Array2D, ArrayList, Random, MonteCarlo_integrate
from cffi import FFI
import os

ffi = FFI()
ffi.cdef("""
    typedef struct {...;} Random_struct, *Random;
    Random new_Random_seed(int seed);
    double Random_nextDouble(Random R);
    double **RandomMatrix(int M, int N, Random R);

    void SOR_execute(int M, int N,double omega, double **G, int num_iterations);
    double MonteCarlo_integrate(int Num_samples);    
    """)
C = ffi.verify("""
    #include <SOR.h>
    #include <Random.h>
    #include <MonteCarlo.h>
    """, 
    extra_compile_args=['-I' + os.path.join(os.getcwd(), 'scimark')],
    extra_link_args=['-fPIC'],
    extra_objects=[os.path.join(os.getcwd(), 'scimark', f) 
                   for f in ['SOR.c', 'Random.c', 'MonteCarlo.c']])

class TestWithArray2D(object):
    Array = Array2D

    def test_SOR(self):
        width, height = 5, 7
        rnd = C.new_Random_seed(7)
        a = C.RandomMatrix(height, width, rnd)
        b = self.Array(width, height, data=a)
        C.SOR_execute(height, width, 1.25, a, 42)
        SOR_execute(1.25, b, 42)
        for x, y in b.indexes():
            assert a[y][x] == b[x, y]

class TestWithArrayList(TestWithArray2D):
    Array = ArrayList

def test_random():
    rnd_C = C.new_Random_seed(7)
    rnd_py = Random(7)
    for i in range(100000):
        assert C.Random_nextDouble(rnd_C) == rnd_py.nextDouble()

def test_montecarlo():
    for n in [100, 200, 500, 1000]:
        assert C.MonteCarlo_integrate(n) == MonteCarlo_integrate(n)


