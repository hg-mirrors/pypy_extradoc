using System;

interface Accumulator
{
  void accumulate(int x);
  int getvalue();
}

class Add: Accumulator
{
  public int value = 0;
  public void accumulate(int x)
  {
    value += x;
  }
  public int getvalue()
  {
    return value;
  }
}

class Count: Accumulator
{
  public int value = 0;
  public void accumulate(int x)
  {
    value++;
  }
  public int getvalue()
  {
    return value;
  }
}

class Test
{
  public static void Main(string[] args)
  {
    int n = Convert.ToInt32(args[0]);
    long start, stop;
    start = DateTime.UtcNow.Ticks;
    int res = accumulator(n);
    stop = DateTime.UtcNow.Ticks;
    double secs = (stop-start) * 1e-7;
    Console.WriteLine("C#:            {0} ({1} seconds)", res, secs);
  }

  public static int accumulator(int n)
  {
    Accumulator acc = null;
    if (n < 0) {
      n = -n;
      acc = new Count();
    }
    else {
      acc = new Add();
    }

    while (n-- > 0) {
      acc.accumulate(n);
    }
    return acc.getvalue();
  }
}
