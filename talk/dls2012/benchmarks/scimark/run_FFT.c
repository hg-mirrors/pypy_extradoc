#include <stdio.h>
#include <assert.h>

#include "Random.c"
#include "FFT.c"

int main(int ac, char **av) {
    assert(ac==3);
    int N = atoi(av[1]);
    int cycles = atoi(av[2]);
    int twoN = 2*N;
    Random R = new_Random_seed(7);
    double *x = RandomVector(twoN, R);
    int i=0;

    for (i=0; i<cycles; i++)
    {
        FFT_transform(twoN, x);     /* forward transform */
        FFT_inverse(twoN, x);       /* backward transform */
    }


    fprintf(stderr, "FFT(%d,%d):    ", N, cycles);
    return 0;
}


