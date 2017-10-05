slides.pdf: slides.tex author.latex
	pdflatex -halt-on-error $<

slides.tex: slides.rst
	rst2beamer.py slides.rst > slides.tex
	sed 's/\\date{}/\\input{author.latex}/' -i slides.tex || exit
	sed 's/\\documentclass\[\]{beamer}/\\documentclass\[aspectratio=169\]{beamer}/' -i slides.tex || exit
