#!/bin/bash
# cronjob.sh

# Activate the virtual environment
source F:\My Folder\Practices\WebScrapper\web_scraper_project\scraper_env\Scripts\activate

# Navigate to the project directory
cd F:\My Folder\Practices\WebScrapper\web_scraper_project

# Run the main script and redirect stdout/stderr to log file
python main.py >> F:\My Folder\Practices\WebScrapper\web_scraper_project\logs\scraper.log 2>&1