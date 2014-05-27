import thread
import sys


lock = thread.allocate_lock()

def workload():
    i = 20000000
    while i:
        i -= 1
    lock.release()

running = range(int(sys.argv[1]))

lock.acquire()
for i in running[:]:
    thread.start_new_thread(workload, ())
lock.acquire()
print "done"
#import os; os._exit(0)
