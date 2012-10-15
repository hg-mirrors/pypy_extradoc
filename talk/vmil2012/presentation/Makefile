talk.pdf: talk.tex
	pdflatex talk.tex &> /dev/null

UNAME := $(shell "uname")
view: talk.pdf
ifeq ($(UNAME), Linux)
	evince talk.pdf &
endif
ifeq ($(UNAME), Darwin)
	open talk.pdf &
endif

