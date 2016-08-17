dyla.pdf: dyla.tex dyla.bib
	pdflatex dyla
	bibtex dyla
	pdflatex dyla
	pdflatex dyla

%.pdf: %.eps
	epstopdf $<

view: dyla.pdf
	xpdf dyla.pdf  &

viewtalk: talk.pdf
	xpdf talk.pdf  &

clean:
	rm dyla.pdf talk.pdf

talk.pdf: talk.tex beamerouterthememy.sty beamerthemeWarsaw.sty
	pdflatex talk

%.pdf: %.eps
	epstopdf $<

