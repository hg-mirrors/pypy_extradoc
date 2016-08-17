from convolution import _conv3, _conv5, _conv3x3, Array2D
from array import array

def test_conv3():
    b = _conv3(array('d', [1, 2, 3, 4, 5, 6, 7, 8, 9]),
               array('d', [-1, 0, 1]))
    assert b == array('d', [-2]) * 7
    
def test_conv5():
    b = _conv5(array('d', [1, 2, 3, 4, 5, 6, 7, 8, 9]),
               array('d', [1, 1, 2, 2, 3]))
    assert b == array('d', [22, 31, 40, 49, 58])
    
def test_conv3x3():
    a = Array2D(5, 5).setup([[11, 12, 13, 14, 15],
                              [21, 22, 23, 24, 25],
                              [31, 32, 33, 34, 35],
                              [41, 42, 43, 44, 45],
                              [51, 52, 53, 54, 55]])
    k = Array2D(3, 3).setup([[1, 2, 3],
                              [1, 1, 2],
                              [2, 1, 1]])
    b = _conv3x3(a, k)
    assert b == Array2D(5, 5).setup([[0,   0,   0,   0, 0],
                                     [0, 326, 340, 354, 0],
                                     [0, 466, 480, 494, 0],
                                     [0, 606, 620, 634, 0],
                                     [0,   0,   0,   0, 0]])

if __name__ == '__main__':
    test_conv3()
    test_conv5()
    test_conv3x3()
