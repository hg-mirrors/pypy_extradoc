

google-talk.pdf: google-talk.txt author.latex title.latex stylesheet.latex
	rst2beamer.py --stylesheet=stylesheet.latex --documentoptions=14pt google-talk.txt google-talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i google-talk.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i google-talk.latex || exit
	pdflatex google-talk.latex  || exit

view: google-talk.pdf
	evince google-talk.pdf &