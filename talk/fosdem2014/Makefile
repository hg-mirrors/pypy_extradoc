# Note to myself (arigo): run in the 64-bit environment

pypy-stm.pdf: pypy-stm.tex
	pdflatex pypy-stm.tex

pypy-stm.tex: pypy-stm.rst
	rst2beamer.py --stylesheet=stylesheet.latex --documentoptions=14pt --input-encoding=utf8 --output-encoding=utf8 $< | python expand-itemize.py > pypy-stm.tex

clean:
	rm -f pypy-stm.tex pypy-stm.pdf
