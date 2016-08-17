import sys

for line in sys.stdin:
    #if line.startswith('\\begin{itemize}'):
    #    line = '\\begin{itemize}\n'
    if line == '\\usepackage[scaled=.90]{helvet}\n':
        line = '\\usepackage[scaled=1.1]{helvet}'
    sys.stdout.write(line)
