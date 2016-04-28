# pip install rst2beamer

# WARNING: to work, it needs this patch for docutils
# https://sourceforge.net/tracker/?func=detail&atid=422032&aid=1459707&group_id=38414

talk.pdf: talk.tex
	pdflatex talk.tex


talk.tex: talk.rst author.latex stylesheet.latex
	rst2beamer --stylesheet=stylesheet.latex --documentoptions=14pt --input-encoding=utf8 --output-encoding=utf8 $<  > talk.tex
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit

