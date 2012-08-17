
from pypy.translator.js import tester
from pypy.translator.js.modules import dom
from serv import HTML, start, exported_methods

def test_js():
    dom.window = dom.Window(HTML)
    dom.document = dom.window.document
    start()
    tester.schedule_callbacks(exported_methods)
    print dom.document.getElementById("s").innerHTML
    assert "Stuff" not in dom.document.getElementById("s").innerHTML
