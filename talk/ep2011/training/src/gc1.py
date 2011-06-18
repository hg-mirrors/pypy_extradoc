def foo():
    f = file('/tmp/bar.txt', 'w')
    f.write('hello world')
    f.close()
    return

foo()
print file('/tmp/bar.txt').read()
