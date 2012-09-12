from reloader import ReloadHack

@ReloadHack
def background(video):
    bkg = fcnt = 0
    for img in video:
        bkg = (fcnt * bkg + img) / (fcnt + 1)
        fcnt += 1
        fg = ((bkg - img) ** 2) > 40
        #yield img
        yield fg * 255
    
    
