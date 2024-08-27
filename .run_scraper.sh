#!/bin/bash
if [ -f run_scraper.sh ]; then
	cp run_scraper.sh .run_scraper.sh
fi
cd ./python/
./venv/bin/python src/main.py

