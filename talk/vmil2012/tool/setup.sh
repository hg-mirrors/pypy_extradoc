#!/bin/bash
VENV=paper_env
if [ ! -d "$VENV" ]; then
    virtualenv "${VENV}"
    source "${VENV}/bin/activate"
    pip install django
    echo "virtualenv created in ${VENV}"
else
    echo "virtualenv already present in ${VENV}"
fi

