talk.pdf: talk.tex figures/data.tex figures/go_data.tex tool/data.py
	pdflatex talk.tex &> /dev/null

UNAME := $(shell "uname")
view: talk.pdf
ifeq ($(UNAME), Linux)
	evince talk.pdf &
endif
ifeq ($(UNAME), Darwin)
	open talk.pdf &
endif


figures/go_data.tex: tool/data.py
figures/data.tex: tool/data.py
	python tool/data.py
