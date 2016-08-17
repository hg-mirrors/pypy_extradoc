from io import mplayer, view
import sys

for img in mplayer(sys.argv[1]):
    view(img)

