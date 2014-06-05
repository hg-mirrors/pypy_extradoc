import threading
import sys
import time
from atomic import hint_commit_soon, atomic

times = []
def workload():
    t = time.time()
    i = 20000000
    while i:
        i -= 1
    times.append(time.time() - t)
    hint_commit_soon()

running = range(int(sys.argv[1]) - 1)

ths = []
for i in running:
    t = threading.Thread(target=workload)
    ths.append(t)
    t.start()

workload()

[u.join() for u in ths]
print times

print "done"
#import os; os._exit(0)
