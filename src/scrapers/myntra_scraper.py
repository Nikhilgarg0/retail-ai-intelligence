from src.scrapers.base_scraper import BaseScraper
from src.utils.helpers import clean_price, clean_rating
from typing import List, Dict, Optional
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyntraScraper(BaseScraper):

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.myntra.com"
        self.platform = "myntra"

    def search_products(self, query: str, max_results: int = 10) -> List[Dict]:
        search_url = f"{self.base_url}/{query.replace(' ', '-')}"
        logger.info(f"Searching Myntra for: {query}")

        html = self.fetch_with_selenium(search_url)
        if not html:
            logger.error("Failed to fetch Myntra search results")
            return []

        soup = self.parse_html(html)
        products = []

        # Myntra product cards sit in <li class="product-base">
        product_items = soup.find_all("li", class_="product-base")
        logger.info(f"Found {len(product_items)} products on page")

        for item in product_items[:max_results]:
            product = self._extract_product_info(item)
            if product:
                products.append(product)

        logger.info(f"✅ Successfully scraped {len(products)} products from Myntra")
        return products

    def _extract_product_info(self, product_item) -> Optional[Dict]:
        try:
            # Product link — all Myntra product cards wrap in <a>
            link_element = product_item.find("a")
            if not link_element:
                return None

            url = self.base_url + "/" + link_element.get("href", "").lstrip("/")

            # Product ID from URL — e.g. /brand/product-name/buy/12345678
            product_id = None
            id_match = re.search(r"/buy/(\d+)", url)
            if id_match:
                product_id = id_match.group(1)

            if not product_id:
                return None

            # Title — brand + product name
            brand = product_item.find("h3", class_="product-brand")
            name = product_item.find("h4", class_="product-product")
            title = None
            if brand and name:
                title = f"{brand.get_text(strip=True)} {name.get_text(strip=True)}"
            elif brand:
                title = brand.get_text(strip=True)

            if not title:
                return None

            # Price — discounted price preferred
            price = None
            price_el = product_item.find("span", class_="product-discountedPrice")
            if not price_el:
                price_el = product_item.find("span", class_="product-price")
            if price_el:
                price = clean_price(price_el.get_text(strip=True))

            # Rating
            rating = None
            rating_el = product_item.find("span", class_="product-ratingsCount")
            if rating_el:
                rating = clean_rating(rating_el.get_text(strip=True))

            # Image
            img_el = product_item.find("img", class_="img-responsive")
            image_url = img_el["src"] if img_el and img_el.get("src") else None

            return {
                "platform": self.platform,
                "product_id": product_id,
                "title": title,
                "price": price,
                "rating": rating,
                "reviews": "0",
                "url": url,
                "image_url": image_url,
                "category": None,
            }

        except Exception as e:
            logger.error(f"Error extracting Myntra product: {e}")
            return None
