talk.pdf: talk.rst author.latex stylesheet.latex
	rst2beamer --stylesheet=stylesheet.latex --overlaybullets=False --documentoptions=14pt talk.rst talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit
	sed 's/XXXFAKETITLE//' -i talk.latex || exit
	#sed 's/\\maketitle/\\input{title.latex}/' -i talk.latex || exit
	pdflatex talk.latex  || exit

view: talk.pdf
	evince talk.pdf &

xpdf: talk.pdf
	xpdf talk.pdf &
