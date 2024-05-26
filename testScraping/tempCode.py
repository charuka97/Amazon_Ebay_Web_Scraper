import yaml
from datetime import datetime
from src.amazon_scraper import scrape_amazon_category
from src.ebay_scraper import scrape_ebay_category
from src.utils import get_amazan_scraper_logger
from src.utils import get_ebay_scraper_logger


# Get Amazon scraper
amazon_logger = get_amazan_scraper_logger()

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

    print(f"Amazon Scraper started at {datetime.now()}")
    amazon_logger.info("Scraper started at %s", datetime.now())

    # collect base url and categories from config and call amazon web scraper separatly from category
    for category in config["amazon"]["categories"]:
        category_url = f"{config['amazon']['base_url']}/{category}"
        scrape_amazon_category(category_url, category)

    print(
        f"Data Scraping from Amazon successfully completed!, Scraper end at {datetime.now()}"
    )
    amazon_logger.info(
        f"Data Scraping from Amazon successfully completed!, \nScraper end at {datetime.now()} \n"
    )

    print(f"Ebay Scraper started at {datetime.now()}")
    ebay_logger.info("Scraper started at %s", datetime.now())

    # collect base url and categories from config and call ebay web scraper separatly from category
    for category in config["ebay"]["categories"]:
        category_url = f"{config['ebay']['base_url']}/{category}"
        scrape_ebay_category(category_url, category)

    print(
        f"Data Scraping from Ebay successfully completed!, Scraper end at {datetime.now()}"
    )
    ebay_logger.info(
        f"Data Scraping from Ebay successfully completed!, \nScraper end at {datetime.now()} \n"
    )


if __name__ == "__main__":
    run_scrapers()

##################################################################################################
import yaml
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from src.amazon_scraper import scrape_amazon_category
from src.ebay_scraper import scrape_ebay_category
from src.utils import get_amazan_scraper_logger, get_ebay_scraper_logger

# Get Amazon scraper logger
amazon_logger = get_amazan_scraper_logger()

# Get Ebay scraper logger
ebay_logger = get_ebay_scraper_logger()


# Capture data from config file
def get_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)


# Called to the config file
config = get_config()


# Called to the multiple scrapers
def run_scrapers():

    # Use ProcessPoolExecutor to create a pool of worker processes.
    with ProcessPoolExecutor() as executor:
        print(f"Amazon Scraper started at {datetime.now()}")
        amazon_logger.info("Scraper started at %s", datetime.now())

        # Create a list of tasks (amazon_futures) for Amazon categories, each submitted to the executor for parallel execution.
        amazon_futures = [
            # This submits a function (scrape_amazon_category or scrape_ebay_category)
            # along with its arguments to the executor.
            # The executor runs these functions concurrently.
            executor.submit(
                scrape_amazon_category,
                f"{config['amazon']['base_url']}/{category}",
                category,
            )
            for category in config["amazon"]["categories"]
        ]

        # Use as_completed to process the results of these tasks as they complete.
        for future in as_completed(amazon_futures):
            future.result()

        print(
            f"Data Scraping from Amazon successfully completed! Scraper ended at {datetime.now()}"
        )
        amazon_logger.info(
            f"Data Scraping from Amazon successfully completed! Scraper ended at {datetime.now()} \n"
        )

        print(f"Ebay Scraper started at {datetime.now()}")
        ebay_logger.info("Scraper started at %s", datetime.now())

        ebay_futures = [
            executor.submit(
                scrape_ebay_category,
                f"{config['ebay']['base_url']}/{category}",
                category,
            )
            for category in config["ebay"]["categories"]
        ]

        for future in as_completed(ebay_futures):
            future.result()

        print(
            f"Data Scraping from Ebay successfully completed! Scraper ended at {datetime.now()}"
        )
        ebay_logger.info(
            f"Data Scraping from Ebay successfully completed! Scraper ended at {datetime.now()} \n"
        )


if __name__ == "__main__":
    run_scrapers()
##################################################################################################
