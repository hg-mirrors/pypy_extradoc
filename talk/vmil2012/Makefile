
jit-guards.pdf: paper.tex paper.bib
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf jit-guards.pdf

view: jit-guards.pdf
	evince jit-guards.pdf &

%.tex: %.py
	pygmentize -l python -o $@ $<
