
jit-guards.pdf: paper.tex paper.bib zotero.bib figures/log.tex figures/example.tex figures/benchmarks_table.tex figures/backend_table.tex figures/ops_count_table.tex figures/resume_data.pdf figures/loop_bridge.pdf figures/guard_table.tex figures/resume_data_table.tex figures/failing_guards_table.tex
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf jit-guards.pdf

print: paper.tex paper.bib zotero.bib figures/log.tex figures/example.tex figures/benchmarks_table.tex figures/backend_table.tex figures/ops_count_table.tex figures/resume_data.eps figures/loop_bridge.eps figures/guard_table.tex figures/resume_data_table.tex figures/failing_guards_table.tex
	latex paper
	bibtex paper
	latex paper
	latex paper
	dvips -t letter paper
	sed -i '' -e "s/paper.dvi/The Efficient Handling of Guards in the Design of RPython's Tracing JIT/g" paper.ps
	ps2pdf -sPAPERSIZE=letter paper.ps	
	mv paper.pdf vmil01-schneider.pdf
	mv paper.ps vmil01-schneider.ps
	@echo "Or run Adobe Distiller"	

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

figures/%_table.tex: tool/build_tables.py logs/backend_summary.csv logs/summary.csv tool/table_template.tex logs/bridge_summary.csv logs/resume_summary.csv logs/guard_summary.json
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

logs/resume_summary.csv: logs/logbench* tool/rdatasize.py
	@if ls logs/logbench* &> /dev/null; then python tool/rdatasize.py logs; fi

logs::
	tool/run_benchmarks.sh

slides:
	$(MAKE) -C presentation

clean:
	rm -f *.aux *.bbl *.blg *.log *.tdo
	rm -f *.pdf
	rm -f *.dvi
	rm -f *.ps
	rm -f figures/*table.tex figures/*table.aux
