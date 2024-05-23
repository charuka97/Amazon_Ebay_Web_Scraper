import yaml
from datetime import datetime
from src.amazon_scraper import scrape_amazon_category
from src.ebay_scraper import scrape_ebay_category
from src.utils import get_amazan_scraper_logger
from src.utils import get_ebay_scraper_logger


# Get Amazon scraper
#amazon_logger = get_amazan_scraper_logger()

# Get Ebay scraper
ebay_logger = get_ebay_scraper_logger()


# capture data from config file
def get_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)


# called to the config file
config = get_config()


# called to the multiple scrappers
def run_scrapers():

    # print(f"Amazon Scraper started at {datetime.now()}")
    # amazon_logger.info("Scraper started at %s", datetime.now())

    # # collect base url and categories from config and call amazon web scraper separatly from category
    # for category in config["amazon"]["categories"]:
    #     category_url = f"{config['amazon']['base_url']}/{category}"
    #     scrape_amazon_category(category_url)

    # print(
    #     f"Data Scraping from Amazon successfully completed!, Scraper end at {datetime.now()}"
    # )
    # amazon_logger.info(
    #     f"Data Scraping from Amazon successfully completed!, \nScraper end at {datetime.now()} \n"
    # )

    print(f"Ebay Scraper started at {datetime.now()}")
    ebay_logger.info("Scraper started at %s", datetime.now())

    # collect base url and categories from config and call ebay web scraper separatly from category
    for category in config["ebay"]["categories"]:
        category_url = f"{config['ebay']['base_url']}/{category}"
        scrape_ebay_category(category_url)

    print(
        f"Data Scraping from Ebay successfully completed!, Scraper end at {datetime.now()}"
    )
    ebay_logger.info(
        f"Data Scraping from Ebay successfully completed!, \nScraper end at {datetime.now()} \n"
    )


if __name__ == "__main__":
    run_scrapers()
