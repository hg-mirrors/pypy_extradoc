import sys

def expand(in_file, out_file):
    for line in in_file:
        line = line.replace(r'\begin{itemize}',
                            r'\begin{itemize}\setlength{\itemsep}{10pt}')
        out_file.write(line)

if __name__ == '__main__':
    expand(sys.stdin, sys.stdout)
