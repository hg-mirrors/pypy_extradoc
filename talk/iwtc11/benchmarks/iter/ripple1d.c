#include <stdio.h>
#include <math.h>
#include <stdlib.h>

double result;

double sum(double *a, int n) {
  int i;
  double sa = 0;
  for (i=0; i<n; i++)  {
    if (sa > a[i]) {
      sa -= 0.1;
    } else if (sa < a[i]) {
      sa += 0.1;
    }
  }
  return sa;
}

#define N 100000000

int main(int ac, char **av) {
  double *a = malloc(N*sizeof(double));
  int i, n = atoi(av[1]);
  double data[] = {-1.0, 1.0};
  for (i=0; i<N; i++) a[i] = data[i&1];
  for (i=0; i<n; i++) result = sum(a, N);
  fprintf(stderr, "sum1d:     ");
  return 0;
}
