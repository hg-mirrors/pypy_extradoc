using System;

class Fibo
{
  public static void Main(string[] args)
  {
    int n = Convert.ToInt32(args[0]);
    long start, stop;
    start = DateTime.UtcNow.Ticks;
    int res = fibo(n);
    stop = DateTime.UtcNow.Ticks;
    double secs = (stop-start) * 1e-7;
    Console.WriteLine("C#:            {0} ({1} seconds)", res, secs);
  }

  public static int fibo(int n)
  {
    int a = 0;
    int b = 1;
    while (--n > 0) {
      int sum = a+b;
      a = b;
      b = sum;
    }
    return b;
  }
}
