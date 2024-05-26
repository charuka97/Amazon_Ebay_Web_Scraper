import src.utils as utils
from src.database import MongoDB, get_config
import random

config = get_config()

def parse_amazon_product_page(soup, productCategory):

    #  s-result-list
    products = []
    product_containers = soup.find_all("div", class_="puis-card-container")

    for container in product_containers:
        product = {}

        # Get product name
        name_element = container.find("span", class_="a-text-normal")
        product["name"] = name_element.text.strip() if name_element else "Not available"

        # Get product price
        price_element = container.find("span", class_="a-offscreen")
        product["price"] = (
            price_element.text.strip() if price_element else "Not available"
        )

        # Get product rating
        rating_element = container.find("span", class_="a-icon-alt")
        product["rating"] = (
            rating_element.text.strip() if rating_element else "Not available"
        )

        # Get number of reviews
        review_count_element = container.find("span", class_="a-size-base")
        product["reviews"] = (
            review_count_element.text.strip() if review_count_element else "0 reviews"
        )

        # Get product images
        image_elements = container.find_all("img", class_="s-image")
        image_urls = []

        for img in image_elements:
            srcset = img.get("srcset", "")
            urls = [url.strip() for url in srcset.split(",")]
            image_urls.extend(urls)
        product["images"] = image_urls

        # Get product category
        product["category"] = productCategory

        products.append(product)

    return products


def scrape_amazon_category(category_url, productCategory):

    db = MongoDB()
    base_url = config["amazon"]["base_url"]
    auth_content = config["amazon"]["auth_content"]

    user_agent = config["amazon"]["User_Agents"]
    headers = config["amazon"]["headers"]

    auth_content["User-Agent"] = random.choice(user_agent)
    auth_content.update(headers)

    soup = utils.fetch_page(category_url, auth_content)
    if soup:
        product_data = utils.handle_pagination(
            soup,
            base_url,
            auth_content,
            lambda soupObj: parse_amazon_product_page(soupObj, productCategory),
        )
        for product in product_data:
            db.insert_item(config["database"]["collections"]["amazon"], product)
    db.close()
