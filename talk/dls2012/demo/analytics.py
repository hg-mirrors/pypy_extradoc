from reloader import ReloadHack
from io import view
from background import Background
from foreground import Foreground

class Tracker(ReloadHack):
    def __init__(self):
        self.bkg = Background()
        self.fg = Foreground()

    def update(self, img):
        background = self.bkg.update(img)
        fg = self.fg.update(img, background)
        view(255*fg)
