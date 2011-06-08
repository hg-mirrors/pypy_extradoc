#include <stdio.h>

#define N 100000000
double a[N], b[N-2];

//void conv(double *a, double *k, double *b) {
void conv(double *__restrict__ a, double *__restrict__ k, double *__restrict__ b) {
  int i;
  for (i=0; i<N-2; i++) {
    b[i] = k[2]*a[i] + k[1]*a[i+1] + k[0]*a[i+2];
  }
}

int main() {
  double k[3] = {-1, 0, 1};
    int i;
    for (i=0; i<N; i++) a[i] = 1;
    conv(a,k, b);
    printf("%f\n", b[N/2]);
    fprintf(stderr, "conv3:         ");
    return 0;
}
