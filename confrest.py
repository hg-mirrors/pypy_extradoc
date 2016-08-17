import py
from confrest_oldpy import *

class PyPyPage(Page): 
    def fill(self):
        super(PyPyPage, self).fill()
        self.menubar[:] = html.div(
            html.a("news", href="/pypy/dist/pypy/doc/news.html", class_="menu"), " ",
            html.a("doc", href="/pypy/dist/pypy/doc/index.html", class_="menu"), " ",
            html.a("contact", href="/pypy/dist/pypy/doc/contact.html", class_="menu"), " ", 
            html.a("getting-started", 
                   href="/pypy/dist/pypy/doc/getting-started.html", class_="menu"), " ",
            html.a("issue", 
                   href="https://codespeak.net/issue/pypy-dev/", 
                   class_="menu"), 
            " ", id="menubar")

    def get_doclink(self, target):
        return relpath(self.targetpath.strpath,
                       self.project.get_docpath().join(target).strpath)

class Project(Project): 
    title = "PyPy" 
    stylesheet = 'http://codespeak.net/pypy/dist/pypy/doc/style.css'
    encoding = 'latin1' 
    prefix_title = "PyPy"
    logo = html.div(
        html.a(
            html.img(alt="PyPy", id="pyimg", 
                     src="http://codespeak.net/pypy/img/py-web1.png", 
                     height=110, width=149)))
    Page = PyPyPage 
    mydir = py.magic.autopath().dirpath()
    def get_docpath(self):
        return self.mydir


