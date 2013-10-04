

view: talk.pdf
	evince talk.pdf

talk.pdf: talk.tex
	64bit pdflatex talk.tex

talk.tex: talk.rst
	rst2beamer --stylesheet=stylesheet.latex --documentoptions=14pt --input-encoding=utf8 --output-encoding=utf8 --overlaybullets=false $< > talk.tex

clean:
	rm -f talk.tex talk.pdf
