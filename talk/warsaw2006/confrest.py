from py.__.documentation.confrest import *

class PyPyFireworksPage(Page): 
    def fill(self):
        super(PyPyFireworksPage, self).fill()
        self.body.attr.onload = 'show()'
        self.menubar[:] = []

class Project(Project):
    title = "PyPy Fireworks" 
    stylesheet = 'style.css'
    encoding = 'latin1' 
    prefix_title = "PyPy "
    logo = html.div(
        html.a(
            html.img(alt="PyPy", id="pyimg", 
                     src="http://codespeak.net/pypy/img/py-web1.png", 
                     height=110, width=149)))
    Page = PyPyFireworksPage

