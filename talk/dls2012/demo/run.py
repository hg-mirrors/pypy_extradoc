from io import mplayer, view
from analytics import Tracker
import sys, time

if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = 'demo.avi'

t0 = time.time()
fcnt = 0

tracker = Tracker()
while True:
    for img in mplayer(fn):
        view(img, 'Input')
        tracker.update(img)

        t1 = time.time()
        if t1 - t0 > 1:
            print >>sys.stderr, '\r%f fps' % (fcnt / (t1-t0)),
            t0 = t1
            fcnt = 0
        fcnt += 1


