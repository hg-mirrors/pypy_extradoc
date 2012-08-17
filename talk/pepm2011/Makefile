# for tikz2pdf: http://codespeak.net/svn/user/antocuni/bin/tikz2pdf

escape-tracing.pdf: paper.tex paper.bib figures/step1.pdf figures/step2.pdf figures/step3.pdf figures/step4.pdf
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper
	mv paper.pdf escape-tracing.pdf

view: escape-tracing.pdf
	evince escape-tracing.pdf &

xpdf: escape-tracing.pdf
	xpdf escape-tracing.pdf &


%.png: %.dot
	dot -Tpng  $< > $@

%.eps: %.dot
	dot -Tps  $< > $@

%.pdf: %.eps
	epstopdf $<

%.pdf: %.tikz
	tikz2pdf -s $<
