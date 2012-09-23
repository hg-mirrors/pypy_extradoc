
from reloader import ReloadHack

class Background(ReloadHack):
    def __init__(self):
        self.image = 0

    def update(self, frame):
        alfa = 0.9
        self.image = alfa * self.image + (1 - alfa) * frame

