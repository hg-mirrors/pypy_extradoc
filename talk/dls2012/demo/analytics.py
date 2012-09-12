from reloader import ReloadHack
from io import view
from background import Background
from foreground import foreground

class Tracker(ReloadHack):
    def __init__(self):
        self.background = Background()

    def update(self, frame):
        self.background.update(frame)
        fg = foreground(frame, self.background.image)
        view(255*fg)
