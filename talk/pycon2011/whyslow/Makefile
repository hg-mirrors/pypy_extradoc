

whyslow-talk.pdf: talk.rst author.latex title.latex stylesheet.latex
	rst2beamer --input-encoding=utf-8 --output-encoding=utf-8 --stylesheet=stylesheet.latex --documentoptions=14pt --theme=Warsaw --overlaybullets=False talk.rst whyslow-talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i whyslow-talk.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i whyslow-talk.latex || exit
	pdflatex whyslow-talk.latex  || exit

view: whyslow-talk.pdf
	evince whyslow-talk.pdf &