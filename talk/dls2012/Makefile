# for tikz2pdf: http://codespeak.net/svn/user/antocuni/bin/tikz2pdf

licm.pdf: paper.tex paper.bib 
	pdflatex paper
	-bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf licm.pdf

view: licm.pdf
	evince licm.pdf &

xpdf: licm.pdf
	xpdf licm.pdf &


%.png: %.dot
	dot -Tpng  $< > $@

%.eps: %.dot
	dot -Tps  $< > $@

%.pdf: %.eps
	epstopdf $<

%.pdf: %.tikz
	tikz2pdf -s $<
