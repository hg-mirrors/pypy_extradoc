# you can find rst2beamer.py and inkscapeslide.py here:
# http://bitbucket.org/antocuni/env/src/619f486c4fad/bin/rst2beamer.py
# http://bitbucket.org/antocuni/env/src/619f486c4fad/bin/inkscapeslide.py


talk.pdf: talk.rst author.latex stylesheet.latex
	rst2beamer --input-encoding=utf8 --output-encoding=utf8 --stylesheet=stylesheet.latex --overlaybullets=False --theme=Boadilla --documentoptions=14pt talk.rst talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i talk.latex || exit
	pdflatex talk.latex  || exit

clean:
	rm talk.pdf talk.latex

view: talk.pdf
	evince talk.pdf &

xpdf: talk.pdf
	xpdf talk.pdf &
