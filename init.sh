#!/bin/bash
#Linux only
cd python/
if [ ! -d venv ]; then
	python -m venv venv
fi
./venv/bin/pip install -r requirements.txt
