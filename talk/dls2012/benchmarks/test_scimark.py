from scimark import SOR_execute, Array2D, ArrayList, Random, MonteCarlo_integrate, LU_factor, \
        FFT_transform, FFT_inverse
from array import array
from cffi import FFI
import os

ffi = FFI()
ffi.cdef("""
    typedef struct {...;} Random_struct, *Random;
    Random new_Random_seed(int seed);
    double Random_nextDouble(Random R);
    double **RandomMatrix(int M, int N, Random R);
    double *RandomVector(int N, Random R);

    void SOR_execute(int M, int N,double omega, double **G, int num_iterations);
    double MonteCarlo_integrate(int Num_samples);    
    int LU_factor(int M, int N, double **A,  int *pivot);
    void FFT_transform(int N, double *data);
    void FFT_inverse(int N, double *data);
    """)
C = ffi.verify("""
    #include <SOR.h>
    #include <Random.h>
    #include <MonteCarlo.h>
    #include <LU.h>
    #include <FFT.h>
    """, 
    extra_compile_args=['-I' + os.path.join(os.getcwd(), 'scimark')],
    extra_link_args=['-fPIC'],
    extra_objects=[os.path.join(os.getcwd(), 'scimark', f) 
                   for f in ['SOR.c', 'Random.c', 'MonteCarlo.c', 'LU.c', 'FFT.c']])

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

    def test_copy_random_matrix(self):
        rnd_C = C.new_Random_seed(7)
        rnd_py = Random(7)
        c_mat = C.RandomMatrix(20, 10, rnd_C)
        py_mat = rnd_py.RandomMatrix(self.Array(10, 20))
        py_mat_cpy = self.Array(10, 20)
        py_mat_cpy.copy_data_from(py_mat)
        for x, y in py_mat.indexes():
            assert c_mat[y][x] == py_mat[x, y] == py_mat_cpy[x, y]


class TestWithArrayList(TestWithArray2D):
    Array = ArrayList

    def test_LU(self):
        rnd = C.new_Random_seed(7)
        for height in [10, 20, 30]:
            for width in [10, 20, 30]:
                c_mat = C.RandomMatrix(height, width, rnd)
                c_pivot = ffi.new('int []', min(width, height))
                py_mat = self.Array(width, height, data=c_mat)
                py_pivot = array('i', [0]) * min(width, height)
                C.LU_factor(height, width, c_mat, c_pivot)
                LU_factor(py_mat, py_pivot)

                for a, b in zip(c_pivot, py_pivot):
                    assert a == b
                for x, y in py_mat.indexes():
                    assert c_mat[y][x] == py_mat[x, y]





def test_random():
    rnd_C = C.new_Random_seed(7)
    rnd_py = Random(7)
    for i in range(100000):
        assert C.Random_nextDouble(rnd_C) == rnd_py.nextDouble()

def test_montecarlo():
    for n in [100, 200, 500, 1000]:
        assert C.MonteCarlo_integrate(n) == MonteCarlo_integrate(n)

def test_fft():
    rnd = C.new_Random_seed(7)
    for n in [256, 512, 1024]:
        data_c = C.RandomVector(n, rnd)
        data_py = array('d', [0.0]) * n
        for i in range(n):
            data_py[i] = data_c[i]
        C.FFT_transform(n, data_c)
        FFT_transform(n, data_py)
        for i in xrange(n):
            assert data_py[i] == data_c[i]
        C.FFT_inverse(n, data_c)
        FFT_inverse(n, data_py)
        for i in xrange(n):
            assert data_py[i] == data_c[i]


