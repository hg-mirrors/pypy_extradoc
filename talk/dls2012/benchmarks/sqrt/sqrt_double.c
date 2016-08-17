#include <stdio.h>

int main() {
  double y = 1234.0;
  double x = y / 2.0;
  long n = 100000000;
  while (n>0) {
    n -= 1;
    x = (x + y/x) / 2.0;
  }
  printf("%f\n", x);
  fprintf(stderr, "sqrt(float):   ");
  return 0;
}
