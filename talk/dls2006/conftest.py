
import py

class Directory(py.test.collect.Directory):
    def run(self):
        l = []
        for x in super(Directory, self).run(): 
            if x in ['draft.txt']: 
                continue
            l.append(x)
        return l
