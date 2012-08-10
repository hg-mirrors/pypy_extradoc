
def test_working():
    assert 1

def test_failing():
    x = [1,2,3]
    assert len(x) == 4

def test_printing():
    print "Blah blah blah blah"

class TestFoo:
    def test_one(self):
        assert 1
