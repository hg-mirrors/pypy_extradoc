
from reloader import ReloadHack

class Background(ReloadHack):
    def __init__(self):
        self.fcnt = 0
        self.image = 0

    def update(self, frame):
        self.fcnt += 1
        alfa = self.fcnt/(self.fcnt + 1.0)
        self.image = alfa * self.image + (1 - alfa) * frame

