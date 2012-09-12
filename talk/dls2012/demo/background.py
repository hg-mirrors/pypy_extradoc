from reloader import ReloadHack

class Background(ReloadHack):
    def __init__(self):
        self.fcnt = self.image = 0

    def update(self, frame):
        self.image = (self.fcnt * self.image + frame) / (self.fcnt + 1)
        self.fcnt += 1

