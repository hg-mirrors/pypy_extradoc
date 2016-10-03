# you can find rst2beamer.py here:
# http://codespeak.net/svn/user/antocuni/bin/rst2beamer.py

# WARNING: to work, it needs this patch for docutils
# https://sourceforge.net/tracker/?func=detail&atid=422032&aid=1459707&group_id=38414

talk.pdf: talk.rst author.latex stylesheet.latex
	rst2beamer.py --stylesheet=stylesheet.latex --documentoptions=14pt --theme=Warsaw --input-encoding=utf8 --output-encoding=utf8 talk.rst talk.latex || exit
	#/home/antocuni/.virtualenvs/rst2beamer/bin/python `which rst2beamer.py` --stylesheet=stylesheet.latex --documentoptions=14pt talk.rst talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit
	#sed 's/\\maketitle/\\input{title.latex}/' -i talk.latex || exit
	pdflatex talk.latex  || exit

view: talk.pdf
	okular talk.pdf

xpdf: talk.pdf
	xpdf talk.pdf &
