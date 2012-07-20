
jit-guards.pdf: paper.tex paper.bib figures/log.tex
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf jit-guards.pdf

UNAME := $(shell "uname")
view: jit-guards.pdf
ifeq ($(UNAME), Linux)
	evince jit-guards.pdf &
endif
ifeq ($(UNAME), Darwin)
	open jit-guards.pdf &
endif

%.tex: %.py
	pygmentize -l python -o $@ $<
