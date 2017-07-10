# you can find rst2beamer.py here:
# http://codespeak.net/svn/user/antocuni/bin/rst2beamer.py

# WARNING: to work, it needs this patch for docutils
# https://sourceforge.net/tracker/?func=detail&atid=422032&aid=1459707&group_id=38414

talk.pdf: talk.rst author.latex stylesheet.latex sobel/CPython-v0.png
	python `which rst2beamer.py` --stylesheet=stylesheet.latex --documentoptions=14pt talk.rst talk.latex || exit

	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit
	pdflatex talk.latex  || exit

sobel/CPython-v0.png: sobel/chart.py
	cd sobel && python chart.py

view: talk.pdf
	evince talk.pdf &

xpdf: talk.pdf
	xpdf talk.pdf &
