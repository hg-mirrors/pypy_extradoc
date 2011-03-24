
jit-hints.pdf: paper.tex paper.bib code/interpreter-slow.tex code/map.tex code/version.tex
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf jit-hints.pdf

view: jit-hints.pdf
	evince jit-hints.pdf &

xpdf: jit-hints.pdf
	xpdf jit-hints.pdf &

%.tex: %.py
	pygmentize -l python -o $@ $<
