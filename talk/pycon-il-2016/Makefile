# pip install rst2beamer

talk.pdf: talk.latex
	pdflatex talk.latex


talk.latex: talk.rst author.latex stylesheet.latex *.png
	rst2beamer --stylesheet=stylesheet.latex --documentoptions=12pt --input-encoding=utf8 --output-encoding=utf8 $<  > talk.latex
	sed 's/\\date{}/\\input{author.latex}/' -i talk.latex || exit

