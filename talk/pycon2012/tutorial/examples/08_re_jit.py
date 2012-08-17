import re
import timeit

welcome = "Welcome to PyCon 2011\n" * 10

inc_year_re = re.compile("(?P<year>\d+)")


def inc_year(m):
    return str(int(m.group('year')) + 1)


simple_re = re.compile("(?P<year>\d+)")


print "simple_replace", timeit.timeit(lambda: simple_re.sub("2012", welcome),
                                      number=10000)

print "inc_replace", timeit.timeit(lambda: inc_year_re.sub(inc_year, welcome),
                                   number=10000)
