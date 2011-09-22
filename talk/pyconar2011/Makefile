

talk.pdf: talk.rst author.latex title.latex stylesheet.latex
	rst2beamer.py --input-encoding=utf-8 --output-encoding=utf-8 --stylesheet=stylesheet.latex --documentoptions=14pt --theme=Warsaw talk.rst talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i talk.latex || exit
	pdflatex talk.latex  || exit

clean:
	rm talk.pdf talk.latex

view: talk.pdf
	evince talk.pdf &
