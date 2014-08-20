
from interp import interp

def test_interp():
    assert interp('ddl\x02', 13) == -1
    assert interp('ddl\x01', 13) == 0
