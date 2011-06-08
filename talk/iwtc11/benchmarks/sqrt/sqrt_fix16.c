#include <stdio.h>

int main() {
  long y = 1234 << 16;
  long x = y / 2;
  long n = 100000000;
  while (n>0) {
    n -= 1;
    x = ((x + (y << 16)/x)) / 2;
  }
  printf("%f\n", ((double) x) / ((double) (1<<16)));
  fprintf(stderr, "sqrt(Fix16):   ");
  return 0;
}
