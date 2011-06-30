# you can find rst2beamer.py here:
# http://codespeak.net/svn/user/antocuni/bin/rst2beamer.py

# WARNING: to work, it needs this patch for docutils
# https://sourceforge.net/tracker/?func=detail&atid=422032&aid=1459707&group_id=38414

talk.pdf: talk.rst author.latex title.latex stylesheet.latex
	rst2beamer.py --input-encoding=utf-8 --output-encoding=utf-8 --stylesheet=stylesheet.latex --documentoptions=14pt talk.rst talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i talk.latex || exit
	pdflatex talk.latex  || exit

teaser.pdf: teaser.rst author.latex title.latex stylesheet.latex
	rst2beamer.py --stylesheet=stylesheet.latex --documentoptions=14pt teaser.rst teaser.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i teaser.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i teaser.latex || exit
	pdflatex teaser.latex  || exit

view: talk.pdf
	evince talk.pdf &

clean:
	rm -f talk.pdf talk.pdf.info talk.aux talk.log talk.nav talk.out talk.snm talk.toc talk.vrb talk.latex

xpdf: talk.pdf
	xpdf talk.pdf &
