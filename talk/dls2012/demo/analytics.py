from reloader import ReloadHack
from io import view
from background import Background
from foreground import foreground

class Tracker(ReloadHack):
    def __init__(self):
        self.bkg = Background()

    def update(self, img):
        background = self.bkg.update(img)
        fg = foreground(img, background)
        view(255*fg)
