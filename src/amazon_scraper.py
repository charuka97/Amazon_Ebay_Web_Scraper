import src.utils as utils
from src.database import MongoDB, get_config
import random
import re
config = get_config()


def parse_amazon_product_page(soup):

    products = []
    product_containers = soup.find_all("div", class_="s-result-item")

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
        product["images"] = (
            [img["src"] for img in image_elements]
            if image_elements
            else ["Not available"]
        )

        # Get product category
        category_element = soup.find("span", class_="a-color-state")
        product["category"] = (
            category_element.text.strip().strip('"/')
            if category_element
            else "Not available"
        )

        products.append(product)

    return products


def scrape_amazon_category(category_url):

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
            soup, base_url, auth_content, parse_amazon_product_page
        )
        for product in product_data:
            db.insert_item(config["database"]["collections"]["amazon"], product)
    db.close()

