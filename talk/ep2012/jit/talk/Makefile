# you can find rst2beamer.py here:
# http://codespeak.net/svn/user/antocuni/bin/rst2beamer.py

# WARNING: to work, it needs this patch for docutils
# https://sourceforge.net/tracker/?func=detail&atid=422032&aid=1459707&group_id=38414

talk.pdf: talk.rst author.latex title.latex stylesheet.latex diagrams/tracing-phases-p0.pdf
	rst2beamer.py --stylesheet=stylesheet.latex --documentoptions=14pt talk.rst talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit
	#sed 's/\\maketitle/\\input{title.latex}/' -i talk.latex || exit
	pdflatex talk.latex  || exit

view: talk.pdf
	evince talk.pdf &

xpdf: talk.pdf
	xpdf talk.pdf &


diagrams/tracing-phases-p0.pdf: diagrams/tracing-phases.svg
	cd diagrams && inkscapeslide.py tracing-phases.svg
