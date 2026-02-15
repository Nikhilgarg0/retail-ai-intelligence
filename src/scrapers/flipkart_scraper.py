# src/scrapers/flipkart_scraper.py
from src.scrapers.base_scraper import BaseScraper
from src.utils.helpers import clean_price, clean_rating
from typing import List, Dict, Optional
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FlipkartScraper(BaseScraper):
    """Scraper specifically for Flipkart India"""

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.flipkart.com"
        self.platform = "flipkart"

    def search_products(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for products on Flipkart

        Args:
            query: Search term (e.g., "wireless headphones")
            max_results: How many products to scrape

        Returns:
            List of product dictionaries
        """
        search_url = f"{self.base_url}/search?q={query.replace(' ', '+')}"
        logger.info(f"Searching Flipkart for: {query}")

        # Fetch the search results page
        html = self.fetch_with_selenium(search_url)

        if not html:
            logger.error("Failed to fetch Flipkart search results")
            return []

        soup = self.parse_html(html)
        products = []

        # Find all product containers (using data-id attribute)
        product_divs = soup.find_all("div", {"data-id": True})
        logger.info(f"Found {len(product_divs)} products on page")

        for div in product_divs[:max_results]:
            product = self._extract_product_info(div)
            if product:
                products.append(product)

        logger.info(f"✅ Successfully scraped {len(products)} products")
        return products

    def _extract_product_info(self, product_div) -> Optional[Dict]:
        """Extract information from a single product card - FIXED VERSION"""
        try:
            # Product ID (from data-id attribute) - CRITICAL
            product_id = product_div.get("data-id")

            if not product_id:
                logger.debug("No product ID found, skipping")
                return None

            # Find the main product link
            link_element = product_div.find("a", class_="GnxRXv")

            if not link_element:
                logger.debug("No link found, skipping product")
                return None

            # Product URL
            url = (
                self.base_url + link_element["href"]
                if link_element and "href" in link_element.attrs
                else None
            )

            # Extract product title from image alt text
            title = None
            img_element = product_div.find("img", class_="UCc1lI")
            if img_element and "alt" in img_element.attrs:
                title = img_element["alt"]

            # If no title from image, try to extract from URL
            if not title and url:
                match = re.search(r"/([^/]+)/p/", url)
                if match:
                    title = match.group(1).replace("-", " ").title()

            if not title:
                logger.debug("No title found, skipping product")
                return None

            # Image URL
            image_url = (
                img_element["src"]
                if img_element and "src" in img_element.attrs
                else None
            )

            # Price - FIXED: Use the correct class
            price = None
            price_element = product_div.find("div", class_="hZ3P6w")

            if price_element:
                price_text = price_element.get_text(strip=True)
                price = clean_price(price_text)

            # Rating - FIXED: Extract from text
            rating = None
            # Flipkart shows rating as plain text, find any text that looks like a rating (e.g., "3.8", "4.2")
            all_text = product_div.get_text()
            # Look for pattern like "3.8" or "4.2" (digit.digit)
            rating_match = re.search(r"\b([0-5]\.\d)\b", all_text)
            if rating_match:
                try:
                    rating = float(rating_match.group(1))
                except ValueError:
                    rating = None

            # Reviews count - Try to find review count
            reviews = "0"
            reviews_element = product_div.find("span", class_="Wphh3N")
            if reviews_element:
                reviews = reviews_element.get_text(strip=True)

            # NEW SCHEMA FORMAT
            product_data = {
                "platform": self.platform,
                "product_id": product_id,  # CRITICAL: Unique ID
                "title": title,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "url": url,
                "image_url": image_url,
                "category": None,  # Will be set when saving
            }

            logger.debug(
                f"Extracted: {title[:50]}... | ID: {product_id} | ₹{price} | {rating}⭐"
            )
            return product_data

        except Exception as e:
            logger.error(f"Error extracting product: {e}")
            return None
