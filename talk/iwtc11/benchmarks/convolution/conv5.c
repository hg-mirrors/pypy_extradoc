#include <stdio.h>
#include <math.h>

#define N 100000000
double a[N], b[N-4];

void conv(double *a, double *k, double *b, int n) {
//void conv(double *__restrict__ a, double *__restrict__ k, double *__restrict__ b, int n) {
  int i;
  for (i=0; i<n-4; i++) {
    b[i] = k[4]*a[i] + k[3]*a[i+1] + k[2]*a[i+2] + k[1]*a[i+3] + k[0]*a[i+4];
  }
}

int main(int ac, char **av) {
    double k[5] = {1, 4, 6, 4, 1};
    int i;
    for (i=0; i<N; i++) a[i] = 1;
    int n = atoi(av[1]);
    for (i=0; i<n; i++)
      conv(a,k, b, N/n);
    printf("%f\n", b[N/2]);
    fprintf(stderr, "conv5(1e%d):     ", ((int) log10(N/n)));
    return 0;
}
