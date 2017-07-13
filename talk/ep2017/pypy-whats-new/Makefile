slides.pdf: slides.tex author.latex
	pdflatex $<

slides.tex: slides.rst
	rst2beamer.py slides.rst > slides.tex
	sed 's/\\date{}/\\input{author.latex}/' -i slides.tex || exit
