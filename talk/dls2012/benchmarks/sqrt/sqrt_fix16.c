#include <stdio.h>

int main() {
  long y = 123 << 16;
  long x = y / 2;
  long n = 100000000;
  while (n>0) {
    n -= 1;
    x = ((x + (y << 8)/(x >> 8))) / 2;
  }
  printf("%f\n", ((double) x) / ((double) (1<<16)));
  fprintf(stderr, "sqrt(Fix16):   ");
  return 0;
}
