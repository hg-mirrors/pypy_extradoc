
from reloader import ReloadHack
from io import view
from background import Background
from foreground import foreground
from detect import find_objects

class Tracker(ReloadHack):
    def __init__(self):
        self.background = Background()

    def update(self, frame):
        self.background.update(frame)
        fg = foreground(frame, self.background.image)
        #view(self.background.image)
        find_objects(fg)
        view(255 * fg)

