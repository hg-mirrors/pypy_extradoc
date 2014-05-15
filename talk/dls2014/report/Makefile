PROJECT=report
TEX=pdflatex
BIBTEX=bibtex
BUILDTEX=$(TEX) $(PROJECT).tex

all:
	$(BUILDTEX)
	$(BIBTEX) $(PROJECT)
	$(BUILDTEX)
	$(BUILDTEX)


clean:
	rm -f *.log *.bak *.aux *.bbl *.blg *.idx *.toc *.out *~
