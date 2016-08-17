open('xxx', 'w').write('stuff')
assert open('xxx').read() == 'stuff'
