from convolution import conv3, conv5
from array import array

def test_conv3():
    b = conv3(array('d', [1, 2, 3, 4, 5, 6, 7, 8, 9]),
              array('d', [-1, 0, 1]))
    assert b == array('d', [-2]) * 7
    
def test_conv5():
    b = conv5(array('d', [1, 2, 3, 4, 5, 6, 7, 8, 9]),
              array('d', [1, 1, 2, 2, 3]))
    assert b == array('d', [22, 31, 40, 49, 58])
    
