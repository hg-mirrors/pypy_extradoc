
#include <stdio.h>
#include <assert.h>

#include "Random.c"
#include "LU.c"
#include "array.c"

int main(int ac, char **av) {
    assert(ac==3);
    int N = atoi(av[1]);
    int cycles = atoi(av[2]);
    double **A = NULL;
    double **lu = NULL; 
    int *pivot = NULL;
    int i;

    Random R = new_Random_seed(7);
    if ((A = RandomMatrix(N, N,  R)) == NULL) exit(1);
    if ((lu = new_Array2D_double(N, N)) == NULL) exit(1);
    if ((pivot = (int *) malloc(N * sizeof(int))) == NULL) exit(1);

    for (i=0; i<cycles; i++)
    {
        Array2D_double_copy(N, N, lu, A);
        LU_factor(N, N, lu, pivot);
    }

    fprintf(stderr, "LU(%d,%d):    ", N, cycles);
    return 0;
}
    
