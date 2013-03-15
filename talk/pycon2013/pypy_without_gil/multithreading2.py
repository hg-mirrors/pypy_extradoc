import thread


def compute(lock):
    global num
    #
    for j in range(10):
        for k in range(10**6):
            pass
        num += 1   # not actually safe!  needs a lock
    #
    lock.release()


num = 0
all_locks = [thread.allocate_lock() for i in range(10)]

for i in range(10):
    lock = all_locks[i]
    lock.acquire()
    thread.start_new_thread(compute, (lock,))

for i in range(10):
    lock = all_locks[i]
    lock.acquire()

print num
