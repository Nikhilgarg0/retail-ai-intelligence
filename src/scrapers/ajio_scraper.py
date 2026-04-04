from src.scrapers.base_scraper import BaseScraper
from src.utils.helpers import clean_price, clean_rating
from typing import List, Dict, Optional
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AjioScraper(BaseScraper):

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.ajio.com"
        self.platform = "ajio"

    def search_products(self, query: str, max_results: int = 10) -> List[Dict]:
        search_url = f"{self.base_url}/search/?text={query.replace(' ', '%20')}"
        logger.info(f"Searching Ajio for: {query}")

        html = self.fetch_with_selenium(search_url)
        if not html:
            logger.error("Failed to fetch Ajio search results")
            return []

        soup = self.parse_html(html)
        products = []

        # Ajio product cards use class "item" inside a results grid
        product_items = soup.find_all("div", class_="item")
        logger.info(f"Found {len(product_items)} products on page")

        for item in product_items[:max_results]:
            product = self._extract_product_info(item)
            if product:
                products.append(product)

        logger.info(f"✅ Successfully scraped {len(products)} products from Ajio")
        return products

    def _extract_product_info(self, product_item) -> Optional[Dict]:
        try:
            # Product link
            link_element = product_item.find("a")
            if not link_element:
                return None

            href = link_element.get("href", "")
            url = self.base_url + href if href.startswith("/") else href

            # Product ID from URL — Ajio URLs end in a product code
            product_id = None
            id_match = re.search(r"/p/([A-Za-z0-9\-]+)$", href)
            if id_match:
                product_id = id_match.group(1)

            if not product_id:
                return None

            # Title — brand name + product name
            brand_el = product_item.find("strong", class_="brand")
            name_el = product_item.find("span", class_="nameCls")
            title = None
            if brand_el and name_el:
                title = f"{brand_el.get_text(strip=True)} {name_el.get_text(strip=True)}"
            elif brand_el:
                title = brand_el.get_text(strip=True)

            if not title:
                return None

            # Price — look for ₹ in any text node
            price = None
            for tag in product_item.find_all(string=re.compile(r"₹")):
                cleaned = clean_price(tag.strip())
                if cleaned and cleaned > 100:
                    price = cleaned
                    break

            # Rating
            rating = None
            rating_el = product_item.find(string=re.compile(r"^\d\.\d$"))
            if rating_el:
                try:
                    rating = float(rating_el.strip())
                except ValueError:
                    pass

            # Image
            img_el = product_item.find("img")
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
            logger.error(f"Error extracting Ajio product: {e}")
            return None
