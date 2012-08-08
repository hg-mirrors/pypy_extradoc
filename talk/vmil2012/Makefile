
jit-guards.pdf: paper.tex paper.bib figures/log.tex figures/example.tex figures/benchmarks_table.tex figures/backend_table.tex figures/ops_count_table.tex figures/loop_bridge.pdf figures/guard_table.tex
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

figures/%_table.tex: tool/build_tables.py logs/backend_summary.csv logs/summary.csv tool/table_template.tex logs/bridge_summary.csv
	tool/setup.sh
	paper_env/bin/python tool/build_tables.py $@

logs/logbench*:;

logs/summary.csv: logs/logbench* tool/difflogs.py
	@if ls logs/logbench* &> /dev/null; then python tool/difflogs.py --diffall logs; fi

logs/backend_summary.csv: logs/logbench* tool/backenddata.py
	@if ls logs/logbench* &> /dev/null; then python tool/backenddata.py logs; fi

logs/bridge_summary.csv: logs/logbench* tool/bridgedata.py
	@if ls logs/logbench* &> /dev/null; then python tool/bridgedata.py logs; fi

logs/guard_summary.json: logs/logbench* tool/guarddata.py
	@if ls logs/logbench* &> /dev/null; then python tool/guarddata.py logs; fi

logs::
	tool/run_benchmarks.sh

clean:
	rm -f *.aux *.bbl *.blg *.log *.tdo
	rm -f *.pdf
	rm -f figures/*table.tex figures/*table.aux
