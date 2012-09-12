from io import mplayer, view
from analytics import Tracker
import sys

if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = 'tv://'

tracker = Tracker()
for img in mplayer(fn):
    view(img)
    tracker.update(img)


