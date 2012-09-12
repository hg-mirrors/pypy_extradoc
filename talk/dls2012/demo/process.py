from reloader import ReloadHack
from fgbg import background

@ReloadHack
def process(video):
    bkg = background(video)
    for img in bkg:
        yield img 


