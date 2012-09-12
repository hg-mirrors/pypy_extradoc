from reloader import ReloadHack

class Background(ReloadHack):
    def __init__(self):
        self.fcnt = self.bkg = 0

    def update(self, img):
        self.bkg = (self.fcnt * self.bkg + img) / (self.fcnt + 1)
        self.fcnt += 1
        return self.bkg

