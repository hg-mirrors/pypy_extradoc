from reloader import ReloadHack

class Foreground(ReloadHack):
    def update(self, img, bkg):
        return ((bkg - img) ** 2) > 100

