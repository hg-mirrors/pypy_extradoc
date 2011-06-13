
// an equivalent using targetmicronumpy is aa+a+a+a+ with the same size

#include <stdlib.h>
#include <stdio.h>

double *create_array(int size)
{
  int i;
  double *a = (double*)malloc(size * sizeof(double));
  for (i = 0; i < size; ++i) {
    a[i] = (double)(i % 10);
  }
  return a;
}

#define MAX 5
#define SIZE 10000000
#define ITERATIONS 10

int main()
{
  double *a[MAX];
  double *res;
  int i, k;

  for (i = 0; i < MAX; ++i) {
    a[i] = create_array(SIZE);
  }
  res = create_array(SIZE);
  // actual loop
  for (k = 0; k < ITERATIONS; ++k) {
    for (i = 0; i < SIZE; ++i) {
      res[i] = a[0][i] + a[1][i] + a[2][i] + a[3][i] + a[4][i];
    }
    printf("%f\n", res[125]); // to kill the optimizer
  }
}
