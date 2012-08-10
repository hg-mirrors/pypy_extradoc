#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "SOR.c"

int main(int ac, char **av) {
    assert(ac==3);
    int N = atoi(av[1]);
    int cycles = atoi(av[2]);
    double **G = malloc(sizeof(double*)*N);
    int i;
    for (i=0; i<N; i++) G[i] = malloc(sizeof(double)*N);
    SOR_execute(N, N, 1.25, G, cycles);
    fprintf(stderr, "SOR(%d, %d):  ", N, cycles);
    return 0;
}
