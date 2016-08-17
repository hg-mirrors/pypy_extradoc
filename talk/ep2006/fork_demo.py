choicepoints = []

def choice():
    child = fork()
    if child is not None:
        choicepoints.append(child)
        return 0
    else:
        return 1

class Fail(Exception):
    pass



invalid_branches = dict.fromkeys([
    (0, 0, 0),
    (0, 0, 1),
    (0, 1),
    (1, 0, 0, 0),
    (1, 0, 0, 0, 0),
    (1, 0, 0, 0, 1),
    (1, 0, 1),
    (1, 1, 0, 0),
    ])

def search():
    path = []
    for i in range(10):
        path.append(choice())
        if tuple(path) in invalid_branches:
            raise Fail
    return path

# ^ ^ ^ that's quite cool code I think :-)
# yes, I agree :-)
# much easier than doing it by hand



# hum, not really RPython, the dict with var-sized tuples
# hum
# we could use lists
# and use a list of lists insteaed of a dict
# good enough
# I can prepare that
# ok, great
# note that fork is a class method or something
# ah, I see
# will just try
# also, I was about to write something like:

search_coro = ...
choicepoints.append(search_coro)

while choicepoints:
    try:
        res = choicepoints.pop().switch()
    except Fail:
        pass
    else:
        print "found it!", res

# is this searching for only one? then we will get (0, )
# no, answers must be 10 numbers long
# ah, I see
# also if we don't add a break after the print, it will
# find all solutions
# oh, right

