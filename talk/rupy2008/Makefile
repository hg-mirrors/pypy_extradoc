%.pdf: %.eps
	epstopdf $<

viewtalk: talk.pdf
	evince talk.pdf  &

clean:
	rm dyla.pdf talk.pdf

talk.pdf: talk.tex beamerouterthememy.sty beamerthemeWarsaw.sty
	pdflatex talk
