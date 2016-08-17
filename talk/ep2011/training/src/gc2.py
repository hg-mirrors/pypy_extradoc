def foo():
    with file('/tmp/bar.txt', 'w') as f:
        f.write('hello world')

foo()
print file('/tmp/bar.txt').read()
