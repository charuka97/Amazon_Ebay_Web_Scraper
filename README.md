# Automated Web Scraper for Amazon and eBay

## Overview
This project includes a Python-based web scraper that collects detailed product information from Amazon and eBay, categorizes products, handles pagination, and runs daily at midnight Sri Lankan time (GMT+5:30).

## Features
- Scrapes product details including name, price, description, rating, number of reviews, images, category, ASIN (Amazon), Item ID (eBay), and seller information.
- Navigates through all categories available on Amazon and eBay.
- Handles multiple pages of product listings.
- Stores data in MongoDB.
- Schedules scraper to run daily at midnight using a cron job.
- Implements robust error handling and logging.

## Installation

### Python Environment Setup
1. Install Python 3.x from [python.org](https://www.python.org/).
2. Create a virtual environment:
   ```sh
   python3 -m venv scraper_env
   source scraper_env/bin/activate  # On Windows use `scraper_env\Scripts\activate`
