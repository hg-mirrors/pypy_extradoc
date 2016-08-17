import os

execfile('test1.py')

def entry_point():
    choicepoints.g_main = ClonableCoroutine()
    choicepoints.g_main.bind(SearchAllTask())
    choicepoints.g_main.switch()
    return 0

# ____________________________________________________________

from pypy.rpython.memory.test.test_transformed_gc import TestStacklessMarkSweepGC
from pypy.translator.c import gc
from pypy.rpython.memory import gctransform


class TGC(TestStacklessMarkSweepGC):
    class gcpolicy(gc.StacklessFrameworkGcPolicy):
        class transformerclass(gctransform.StacklessFrameworkGCTransformer):
            GC_PARAMS = {'start_heap_size': 99999999 }


if __name__ == '__main__':
    gctest = TGC()
    run = gctest.runner(entry_point)
    run([])
