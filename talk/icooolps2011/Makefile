
jit-hints.pdf: paper.tex paper.bib
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf jit-hints.pdf

view: jit-hints.pdf
	evince jit-hints.pdf &

xpdf: jit-hints.pdf
	xpdf jit-hints.pdf &
