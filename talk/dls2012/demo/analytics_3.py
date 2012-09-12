from reloader import ReloadHack
from io import view
from background import Background

class Tracker(ReloadHack):
    def __init__(self):
        self.bkg = Background()

    def update(self, img):
        background = self.bkg.update(img)
        view(background)
