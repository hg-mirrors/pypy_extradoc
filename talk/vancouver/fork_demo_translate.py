from pypy.module._stackless.interp_coroutine import AbstractThunk
from pypy.module._stackless.interp_clonable import InterpClonableCoroutine
import os

class ChoicePointHolder(object):
    def __init__(self):
        self.choicepoints = []
        self.clone_me = False
        self.answer = 0

    def next_choice(self):
        return self.choicepoints.pop()

    def add(self, choice, answer=0):
        self.choicepoints.append((choice, answer))

    def more_choices(self):
        return bool(self.choicepoints)

    def choice(self):
        os.write(1, "choice\n")
        self.clone_me = True
        g_main.switch()
        return self.answer

choicepoints = ChoicePointHolder()
g_main = InterpClonableCoroutine.getmain()

class Fail(Exception):
    pass

# ____________________________________________________________

invalid_branches = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 0, 1],
    [1, 1, 0, 0],
    ]

class SearchTask(AbstractThunk):
    def call(self):
        path = []
        for i in range(10):
            path.append(choicepoints.choice())
            os.write(1, "trying: %s" % path)
            if path in invalid_branches:
                os.write(1, " NO\n")
                raise Fail
            os.write(1, " yes\n")
        os.write(1, "found a solution: %s\n" % path)


def search_all(argv):
    search_coro = InterpClonableCoroutine()
    search_coro.bind(SearchTask())
    choicepoints.add(search_coro)

    os.write(1, "starting\n")
    while choicepoints.more_choices():
        searcher, nextvalue = choicepoints.next_choice()
        choicepoints.clone_me = False
        choicepoints.answer = nextvalue
        try:
            searcher.switch()
        except Fail:
            assert not choicepoints.clone_me
        else:
            if choicepoints.clone_me:
                searcher2 = searcher.clone()
                choicepoints.add(searcher, 1)
                choicepoints.add(searcher2, 0)
    return 0

def target(*args):
    return search_all, None
