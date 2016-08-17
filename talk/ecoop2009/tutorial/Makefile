%.pdf: %.tex %.bib
	pdflatex $<
	bibtex $*
	pdflatex $<
	pdflatex $<

auto: proposal.pdf

clean:
	rm -f *.bbl *.aux *.log *.blg *.pdf
