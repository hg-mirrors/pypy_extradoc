
pypy-jit.pdf: paper.tex paper.bib
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf pypy-jit.pdf

view: pypy-jit.pdf
	evince pypy-jit.pdf &

xpdf: pypy-jit.pdf
	xpdf pypy-jit.pdf &
