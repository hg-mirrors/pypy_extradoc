
pypy-talk.pdf: talk.rst author.latex title.latex stylesheet.latex
	rst2beamer --input-encoding=utf-8 --output-encoding=utf-8 --stylesheet=stylesheet.latex --documentoptions=14pt --theme=Warsaw --overlaybullets=False talk.rst pypy-talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i pypy-talk.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i pypy-talk.latex || exit
	pdflatex pypy-talk.latex  || exit

view: pypy-talk.pdf
	evince pypy-talk.pdf &