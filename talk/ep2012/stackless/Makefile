# you can find rst2beamer.py here:
# http://codespeak.net/svn/user/antocuni/bin/rst2beamer.py

slp-talk.pdf: slp-talk.rst author.latex title.latex stylesheet.latex
	rst2beamer.py --stylesheet=stylesheet.latex --documentoptions=14pt slp-talk.rst slp-talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i slp-talk.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i slp-talk.latex || exit
	sed 's/\\usepackage\[latin1\]{inputenc}/\\usepackage[utf8]{inputenc}/' -i slp-talk.latex || exit
	pdflatex slp-talk.latex  || exit

view: slp-talk.pdf
	evince talk.pdf &

xpdf: slp-talk.pdf
	xpdf slp-talk.pdf &
