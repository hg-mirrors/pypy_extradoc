from io import mplayer, view
from process import process
import sys

if len(sys.argv) > 1:
    video = mplayer(sys.argv[1])
else:
    video = mplayer()

result = process(video)

for img in result:
    view(img)


