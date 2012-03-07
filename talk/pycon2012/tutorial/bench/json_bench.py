import time
import json

# execution runtime per test case
TARGET_RUNTIME = 10

EMPTY = ({}, 200000)
SIMPLE = ({'key1': 0, 'key2': True, 'key3': 'value', 'key4': 'foo', 'key5': 'string'}, 100000)
NESTED = ({'key1': 0, 'key2': SIMPLE[0], 'key3': 'value', 'key4': SIMPLE[0], 'key5': SIMPLE[0], u'key': u'\u0105\u0107\u017c'}, 100000)
HUGE = ([NESTED[0]] * 1000, 100)

cases = ['EMPTY', 'SIMPLE', 'NESTED', 'HUGE']

def main(n):
    l = []
    for i in range(n):
        t0 = time.time()
        for case in cases:
            data, count = globals()[case]
            for i in range(count):
                json.dumps(data)
            print time.time() - t0
        l.append(time.time() - t0)
    return l

if __name__ == '__main__':
    main(1)
