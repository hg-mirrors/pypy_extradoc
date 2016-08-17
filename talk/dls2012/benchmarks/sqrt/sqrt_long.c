#include <stdio.h>

int main() {
  long y = 1234;
  long x = y / 2;
  long n = 100000000;
  while (n>0) {
    n -= 1;
    x = (x + y/x) / 2;
  }
  printf("%d\n", x);
  fprintf(stderr, "sqrt(int):     ");
  return 0;
}
