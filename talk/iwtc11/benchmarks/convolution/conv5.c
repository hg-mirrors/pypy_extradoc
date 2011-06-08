#include <stdio.h>

#define N 100000000
double a[N], b[N-4];

//void conv(double *a, double *k, double *b) {
void conv(double *__restrict__ a, double *__restrict__ k, double *__restrict__ b) {
  int i;
  for (i=0; i<N-4; i++) {
    b[i] = k[4]*a[i] + k[3]*a[i+1] + k[2]*a[i+2] + k[1]*a[i+3] + k[0]*a[i+4];
  }
}

int main() {
    double k[5] = {1, 4, 6, 4, 1};
    int i;
    for (i=0; i<N; i++) a[i] = 1;
    conv(a,k, b);
    printf("%f\n", b[N/2]);
    fprintf(stderr, "conv5:         ");
    return 0;
}
