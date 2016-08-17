talk.pdf: talk.rst stylesheet.latex author.latex
	rst2beamer --stylesheet=stylesheet.latex --documentoptions=14pt talk.rst talk.latex --overlaybullets=false || exit
	pdflatex talk.latex

clean:
	rm talk.pdf talk.latex