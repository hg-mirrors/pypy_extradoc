import dis

def fn(n):
    tot = 0
    while n:
        tot += n
        n -= 1
    return tot

dis.dis(fn)
