from array import array

def conv3(a, k):
    assert len(k)==3
    b = array(a.typecode, [0]) * (len(a) - 2)
    for i in xrange(len(b)):
        b[i] = k[2]*a[i] + k[1]*a[i+1] + k[0]*a[i+2]
    return b

def conv5(a, k):
    assert len(k)==5
    b = array(a.typecode, [0]) * (len(a) - 4)
    for i in xrange(len(b)):
        b[i] = k[4]*a[i] + k[3]*a[i+1] + k[2]*a[i+2] + k[1]*a[i+3] + k[0]*a[i+4]
    return b
