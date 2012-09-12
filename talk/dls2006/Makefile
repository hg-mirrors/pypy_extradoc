
pypy-vm-construction.pdf: paper.tex paper.bib image/*.pdf
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf pypy-vm-construction.pdf

view: pypy-vm-construction.pdf
	xpdf pypy-vm-construction.pdf &
