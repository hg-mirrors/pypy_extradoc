#include <stdio.h>
#include <assert.h>

#include "Random.c"
#include "MonteCarlo.c"

int main(int ac, char **av) {
    assert(ac==2);
    int N = atoi(av[1]);
    MonteCarlo_integrate(N);
    fprintf(stderr, "MonteCarlo(%d):    ", N);
    return 0;
}


