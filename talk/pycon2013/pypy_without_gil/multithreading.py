import thread


def compute(lock):
    #
    for k in xrange(10**7):
        pass
    #
    lock.release()


all_locks = [thread.allocate_lock() for i in range(10)]

for i in range(10):
    lock = all_locks[i]
    lock.acquire()
    thread.start_new_thread(compute, (lock,))

for i in range(10):
    lock = all_locks[i]
    lock.acquire()
