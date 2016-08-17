// A safe array example.
#include <stdio.h>
#include <stdlib.h>

class Array2D {
  double *data;
public:
  int width, height;
  Array2D(int w, int h) {
    width = w;
    height = h;
    data = (double *) malloc(w*h*sizeof(double));
  }
  double &operator()(int x, int y) {
    if (x >= 0 && x < width && y >= 0 && y < height) {
	return data[y*width + x];
    }
    printf("IndexError\n");
    exit(1);
  }
};

#define max(x,y) ((x) > (y) ? (x) : (y))

void dilate3x3(Array2D &a, Array2D &k, Array2D &b) {
  int x, y;
  for (y=1; y<a.height-1; y++) {
    for (x=1; x<a.width-1; x++) {
      double v = k(2,2)*a(x-1, y-1);
      v = max(v, k(1,2)*a(x, y-1));
      v = max(v, k(0,2)*a(x+1, y-1));
      v = max(v, k(2,1)*a(x-1, y));
      v = max(v, k(1,1)*a(x, y));
      v = max(v, k(0,1)*a(x+1, y));
      v = max(v, k(2,0)*a(x-1, y+1));
      v = max(v, k(1,0)*a(x, y+1));
      v = max(v, k(0,0)*a(x+1, y+1));
      b(x, y) = v;
    }
  }
}

int main(int ac, char **av) {
  int w = atoi(av[1]), h = atoi(av[2]);
  int i;

  for (i=0; i<10; i++) {
    Array2D a(w, h), b(w, h), k(3, 3);
    dilate3x3(a, k, b);
    printf("%f\n", b(1,1));
  }
  fprintf(stderr, "dilate3x3(%d):  ", h);
  return 0;
}
