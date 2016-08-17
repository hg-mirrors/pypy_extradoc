"""
fix_usermap <authormap> <fixups>
:takes a name: realmail listing, fixes up a authormap (see usermap.txt)

"""
import sys

fixups = {}
with open(sys.argv[2]) as fp:
    for line in fp:
        try:
            name, mail = line.split(':')
            fixups[name.strip()] = mail.strip()
        except ValueError:
            pass
            

with open(sys.argv[1]) as fp:
    for line in fp:
        if 'codespeak.net' not in line:
            sys.stdout.write(line)
        else:
            before = line.split('<')[0]
            name = line.split('=')[0]
            if name in fixups:
                sys.stdout.write('%s<%s>\n'% (before, fixups[name]))
            else:
                sys.stdout.write(line)
                sys.stderr.write('didnnt find %s\n'%name)

