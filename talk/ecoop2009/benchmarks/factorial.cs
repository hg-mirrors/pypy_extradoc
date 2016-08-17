using System;

class Factorial
{
  public static void Main(string[] args)
  {
    int n = Convert.ToInt32(args[0]);

    long start, stop;
    start = DateTime.UtcNow.Ticks;
    int res = factorial(n);
    stop = DateTime.UtcNow.Ticks;
    double secs = (stop-start) * 1e-7;
    Console.WriteLine("C#:            {0} ({1} seconds)", res, secs);
  }

  public static int factorial(int n)
  {
    int res=1;
    for(int i=1; i<=n; i++)
      res *= i;
    return res;
  }
}
