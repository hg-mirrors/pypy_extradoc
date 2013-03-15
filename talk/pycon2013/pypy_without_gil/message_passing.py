import thread, Queue


def compute(queue):
    #
    for j in range(10):
        for k in range(10**6):
            pass
        queue.put(1)
    #
    queue.put("done")


queue = Queue.Queue()
for i in range(10):
    thread.start_new_thread(compute, (queue,))

running_threads = 10
num = 0

while running_threads > 0:
    item = queue.get()
    if item == "done":
        running_threads -= 1
    else:
        num += 1

print num
