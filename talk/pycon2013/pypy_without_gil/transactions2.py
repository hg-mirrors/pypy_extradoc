import transaction


def do_stuff(x):
    # huge piece of code doing tons of messy things
    for j in range(10**6):
        assert x != 42


def do_stuff_for_all(lst):
    for x in lst:
        do_stuff(x)
    #for x in lst:
    #    transaction.add(do_stuff, x)
    #transaction.run()


do_stuff_for_all(range(20))
