from reloader import ReloadHack

@ReloadHack
def process(video):
    for img in video:
        yield img * 2 


