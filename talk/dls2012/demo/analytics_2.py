from reloader import ReloadHack
from io import view

class Tracker(ReloadHack):
    def update(self, img):
        view(2 * img, 'bkg')
