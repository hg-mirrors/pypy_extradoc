
jit-guards.pdf: paper.tex paper.bib figures/log.tex figures/example.tex figures/benchmarks_table.tex
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

figures/benchmarks_table.tex: tool/build_tables.py logs/summary.csv tool/table_template.tex
	python tool/build_tables.py logs/summary.csv tool/table_template.tex figures/benchmarks_table.tex

logs/summary.csv: tool/difflogs.py
	python tool/difflogs.py --diffall logs
