

google-talk.pdf: google-talk.txt author.latex title.latex stylesheet.latex
	rst2beamer --input-encoding=utf-8 --output-encoding=utf-8 --stylesheet=stylesheet.latex --documentoptions=14pt --theme=Warsaw --overlaybullets=False google-talk.txt google-talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i google-talk.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i google-talk.latex || exit
	pdflatex google-talk.latex  || exit

mozilla-talk.pdf: mozilla-talk.txt author.latex title.latex stylesheet.latex
	rst2beamer --input-encoding=utf-8 --output-encoding=utf-8 --stylesheet=stylesheet.latex --documentoptions=14pt --theme=Warsaw --overlaybullets=False mozilla-talk.txt mozilla-talk.latex || exit
	sed 's/\\date{}/\\input{author.latex}/' -i mozilla-talk.latex || exit
	sed 's/\\maketitle/\\input{title.latex}/' -i mozilla-talk.latex || exit
	pdflatex mozilla-talk.latex  || exit

view: google-talk.pdf
	evince google-talk.pdf &