from reloader import autoreload

@autoreload
def foreground(img, bkg):
    return ((bkg - img) ** 2) > 100

