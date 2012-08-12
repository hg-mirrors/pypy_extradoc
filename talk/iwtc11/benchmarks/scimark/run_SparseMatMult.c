#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "SparseCompRow.c"

int main(int ac, char **av) {
    assert(ac==4);
    int N = atoi(av[1]);
    int nz = atoi(av[2]);
    int cycles = atoi(av[3]);
    
        double *x = (double*) malloc(sizeof(double)*N); //RandomVector(N, R);
        double *y = (double*) malloc(sizeof(double)*N);

        double result = 0.0;

        int nr = nz/N;      /* average number of nonzeros per row  */
        int anz = nr *N;    /* _actual_ number of nonzeros         */

            
        double *val = (double *) malloc(sizeof(double)*anz); //RandomVector(anz, R);
        int *col = (int*) malloc(sizeof(int)*nz);
        int *row = (int*) malloc(sizeof(int)*(N+1));
        int r=0;

        row[0] = 0; 
        for (r=0; r<N; r++)
        {
            /* initialize elements for row r */

            int rowr = row[r];
            int step = r/ nr;
            int i=0;

            row[r+1] = rowr + nr;
            if (step < 1) step = 1;   /* take at least unit steps */


            for (i=0; i<nr; i++)
                col[rowr+i] = i*step;
                
        }

    SparseCompRow_matmult(N, y, val, row, col, x, cycles);
    fprintf(stderr, "SparseMatMult(%d, %d, %d):  ", N, nz, cycles);
    return 0;
}


