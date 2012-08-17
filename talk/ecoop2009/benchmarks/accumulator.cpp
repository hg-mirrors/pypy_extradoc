
#include <stdlib.h>
#include <iostream>
#include <sys/time.h>

class Accumulator
{
 public:
  virtual void accumulate(int x) = 0;
  virtual int getvalue() = 0;
};

class Add : public Accumulator
{
  int value;
public:
  Add()
  {
    value = 0;
  }

  virtual void accumulate(int x)
  {
    value += x;
  }
  virtual int getvalue()
  {
    return value;
  }
};

class Count : public Accumulator
{
  int value;
public:
  Count()
  {
    value = 0;
  }
  virtual void accumulate(int x)
  {
    value++;
  }
  virtual int getvalue()
  {
    return value;
  }
};

int accumulator(int n)
{
  Accumulator* acc = NULL;
  int res;

  if (n < 0) {
    n = -n;
    acc = new Count();
  } else {
    acc = new Add();
  }
  while (n-- > 0) {
    acc->accumulate(n);
  }
  res = acc->getvalue();
  delete acc;
  return res;
}


int main(int argc, char **argv)
{
  int arg, res;
  struct timeval t0, t1;
  double time;
  
  arg = atoi(argv[1]);
  gettimeofday(&t0, NULL);
  res = accumulator(arg);
  gettimeofday(&t1, NULL);
  time = ((t1.tv_sec + ((float)t1.tv_usec / 1000000)) -
          (t0.tv_sec + ((float)t0.tv_usec / 1000000)));
  std::cout << "C++ " << res << " " << time << "\n";
}
