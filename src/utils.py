import requests
from bs4 import BeautifulSoup
import time
import random
from src.database import get_config
import logging

config = get_config()

# The backoff_factor in fetch_page increases the delay after each failed attempt, 
# which is especially useful for handling rate limiting.
def fetch_page(url, auth_content, retries=5, backoff_factor=0.3):

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


def handle_pagination(soup, base_url, auth_content, parse_function, category='Unkonwn'):
    
    # product_data for store the data of all products scraped across multiple pages.
    product_data = []
    next_url = ""
    page_number = 1

    while True:
        # Passed soup to the scrapper function to scrape data of 
        # current page and then adedd to the product_data list until pagination end
        product_data.extend(parse_function(soup))

        # Make next page for pagination
        if base_url == config["ebay"]["base_url"]:
            current_page_element = soup.find("a", class_="pagination__item")

            if current_page_element:
                next_url = f"{base_url}/{category}?rt=nc&_pgn={page_number}"
                page_number += 1
            else:
                break

        elif base_url == config["amazon"]["base_url"]:
            next_page_element = soup.find("a", class_="s-pagination-next")
            
            # Checks if the next page element is found and is not disabled. If both conditions are true, 
            # it indicates that there is another page to scrape.
            if next_page_element and "disabled" not in next_page_element.get("class", []):
                next_url = f"{base_url}{next_page_element['href']}"
            else:
                break  # No next page found or it is disabled, end pagination

        else:
            break  # Unsupported base_url

        print(f"Next URL: {next_url}")
        
        # Fetches the next page using the fetch_page function and updates the soup object with the new page's content.
        soup = fetch_page(next_url, auth_content)

        if soup is None:
            break
        time.sleep(random.uniform(1, 3)) # Random delay between requests

    # Returns the list of all product data collected from all the pages.
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
