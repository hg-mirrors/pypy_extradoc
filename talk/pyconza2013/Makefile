

view: talk.pdf
	xpdf talk.pdf

talk.pdf: talk.tex
	64bit pdflatex talk.tex

talk.tex: talk1.tex fix.py
	python fix.py < talk1.tex > talk.tex

talk1.tex: talk.rst
	rst2beamer $< > talk1.tex
