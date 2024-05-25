import src.utils as utils
from src.database import MongoDB, get_config
import random

config = get_config()


def parse_individual_product_page(product_url, headers):
    product_soup = utils.fetch_page(product_url, headers)
    if not product_soup:
        return None

    product = {}

    # Get product name
    name_element = product_soup.find("h1", class_="product-title")
    product["name"] = name_element.text.strip() if name_element else "Not available"

    # Get product price
    price_element = product_soup.find("span", class_="price")
    product["price"] = price_element.text.strip() if price_element else "Not available"

    # Get product rating
    rating_element = product_soup.find("span", class_="rating")
    product["rating"] = (
        rating_element.text.strip() if rating_element else "Not available"
    )

    # Get number of reviews
    review_count_element = product_soup.find("span", class_="review-count")
    product["reviews"] = (
        review_count_element.text.strip() if review_count_element else "0 reviews"
    )

    # Get product images
    image_elements = product_soup.find_all("img", class_="product-image")
    product["images"] = (
        [img["src"] for img in image_elements] if image_elements else ["Not available"]
    )

    return product


def parse_alibaba_product_page(soup, productCategory, headers):
    products = []
    product_containers = soup.find_all("div", class_="fy23-search-card")

    for container in product_containers:
        # Extract product URL
        url_element = container.find("a", class_="search-card-e-title")
        product_url = f"https:{url_element['href']}" if url_element else None

        if product_url:
            product = parse_individual_product_page(product_url, headers)
            if product:
                product["category"] = productCategory
                products.append(product)

    return products


def scrape_alibaba_category(category_url, productCategory):
    db = MongoDB()
    base_url = config["alibaba"]["base_url"]
    headers = config["alibaba"]["headers"]
    headers["User-Agent"] = random.choice(config["alibaba"]["User_Agents"])

    soup = utils.fetch_page(category_url, headers)
    if soup:
        product_data = utils.handle_pagination(
            soup,
            base_url,
            headers,
            lambda soupObj: parse_alibaba_product_page(
                soupObj, productCategory, headers
            ),
        )
        for product in product_data:
            db.insert_item(config["database"]["collections"]["alibaba"], product)
    db.close()




#  503 Server Error: Service Unavailable for url: https://www.ebay.com/b/Mens-Shoes/93427/bn_61999?rt=nc&_pgn=36
# Retrying in 0.3656791899729975 seconds due to 503 error...