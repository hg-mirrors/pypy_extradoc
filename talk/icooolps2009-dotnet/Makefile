
cli-jit.pdf: *.tex paper.bib *.png blockid.pdf
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf cli-jit.pdf

view: cli-jit.pdf
	evince cli-jit.pdf &

xpdf: cli-jit.pdf
	xpdf cli-jit.pdf &
