import requests
from bs4 import BeautifulSoup
import time
import random
import yaml
import logging

# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.1.2 Safari/602.3.12",
# ]

# HEADERS = {
#     "Accept-Encoding": "gzip, deflate",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "DNT": "1",
#     "Connection": "close",
#     "Upgrade-Insecure-Requests": "1",
# }


def fetch_page(url, auth_content, retries=1, backoff_factor=0.3):

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=auth_content)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")

        except requests.exceptions.RequestException as e:

            print(f"Failed to fetch page {url}: {e}")

            if response.status_code == 503:
                sleep_time = backoff_factor * (2**attempt) + random.uniform(0, 0.5)
                print(f"Retrying in {sleep_time} seconds due to 503 error...")
                time.sleep(sleep_time)
            else:
                return None


def handle_pagination(soup, base_url, auth_content, parse_function):

    product_data = []

    while True:

        product_data.extend(parse_function(soup))
        next_page = soup.find("a", class_="s-pagination-next")

        if not next_page or "disabled" in next_page.get("class", []):
            break
        next_url = f"{base_url}{next_page['href']}"
        soup = fetch_page(next_url, auth_content)

        if soup is None:
            break
        time.sleep(random.uniform(1, 3))

    return product_data


# Configure logging for Amazon scraper
def get_amazan_scraper_logger():
    amazon_logger = logging.getLogger("AmazonScraper")
    amazon_logger.setLevel(logging.INFO)
    amazon_handler = logging.FileHandler("logs/amazonScraperLogs.log")
    amazon_formatter = logging.Formatter("%(message)s")
    amazon_handler.setFormatter(amazon_formatter)
    amazon_logger.addHandler(amazon_handler)

    return amazon_logger


# Configure logging for eBay scraper
def get_ebay_scraper_logger():
    ebay_logger = logging.getLogger("EbayScraper")
    ebay_logger.setLevel(logging.INFO)
    ebay_handler = logging.FileHandler("logs/ebayScraperLogs.log")
    ebay_formatter = logging.Formatter("%(message)s")
    ebay_handler.setFormatter(ebay_formatter)
    ebay_logger.addHandler(ebay_handler)

    return ebay_logger
