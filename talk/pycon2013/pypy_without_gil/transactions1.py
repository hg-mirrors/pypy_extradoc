import transaction



class MyStuff(object):
    counter = 0

def increment_class_counter():
    MyStuff.counter += 1


def compute():
    for j in range(10):
        for k in range(10**6):
            pass
        transaction.add(increment_class_counter)


for i in range(10):
    transaction.add(compute)

transaction.run()

print MyStuff.counter
