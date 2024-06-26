import src.utils as utils
from src.database import MongoDB, get_config
import random

config = get_config()


def parse_ebay_product_page(soup, productCategory):

    products = []
    product_containers = soup.find_all("li", class_="s-item")

    for container in product_containers:

        product = {}
        # Get product name
        name_element = container.find("h3", class_="s-item__title")
        product["name"] = name_element.text.strip() if name_element else "Not available"

        # Get product price
        price_element = container.find("span", class_="s-item__price")
        product["price"] = (
            price_element.text.strip() if price_element else "Not available"
        )

        # Get shipping price
        shipping_element = container.find("span", class_="s-item__shipping")
        product["shipping"] = (
            shipping_element.text.strip() if shipping_element else "Not available"
        )

        # # Get product image
        image_grid_container = soup.find("div", class_="s-item__image-helper")
        image_links = []
        if image_grid_container:
            img_elements = image_grid_container.select(".s-item__image-img")
            image_links = [img["src"] for img in img_elements if "src" in img.attrs]
        product["images"] = image_links

        # Get product categorycategory_element = soup.find("h1", class_="srp-controls__count-heading")
        product["category"] = productCategory

        products.append(product)

    return products


def scrape_ebay_category(category_url, productCategory):

    db = MongoDB()
    base_url = config["ebay"]["base_url"]
    auth_content = config["ebay"]["auth_content"]

    headers = config["ebay"]["headers"]
    user_agent = config["ebay"]["User_Agents"]

    auth_content["User-Agent"] = random.choice(user_agent)
    auth_content.update(headers)

    soup = utils.fetch_page(category_url, auth_content)
    if soup:
        product_data = utils.handle_pagination(
            soup,
            base_url,
            auth_content,
            lambda soupObj: parse_ebay_product_page(soupObj, productCategory),
            productCategory,
        )
        for product in product_data:
            db.insert_item(config["database"]["collections"]["ebay"], product)
    db.close()
