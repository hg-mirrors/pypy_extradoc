

slides.pdf: slides.rst author.latex title.latex stylesheet.latex
	rst2beamer.py --input-encoding=utf-8 --output-encoding=utf-8 --stylesheet=stylesheet.latex --documentoptions=14pt --theme=Warsaw slides.rst slides.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i slides.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i slides.latex || exit
	pdflatex slides.latex  || exit

view: slides.pdf
	evince slides.pdf &

clean:
	rm -f slides.pdf slides.latex
