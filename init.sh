#!/bin/bash
#Linux only
cp .run_scraper.sh run_scraper.sh
cd python/
if [ ! -d venv ]; then
	python -m venv venv
fi
./venv/bin/pip install -r requirements.txt
