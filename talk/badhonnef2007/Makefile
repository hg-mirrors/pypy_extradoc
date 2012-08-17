badhonnef.pdf: badhonnef.tex badhonnef.bib
	pdflatex badhonnef
	bibtex badhonnef
	pdflatex badhonnef
	pdflatex badhonnef

%.pdf: %.eps
	epstopdf $<

view: badhonnef.pdf
	xpdf badhonnef.pdf  &

clean:
	rm badhonnef.pdf

