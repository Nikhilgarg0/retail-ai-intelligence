# src/scrapers/base_scraper.py
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import settings
from src.utils.helpers import random_delay
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper:
    """Base class for all web scrapers"""

    def __init__(self):
        self.delay = settings.scrape_delay
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def setup_driver(self):
        """Setup Selenium WebDriver with Chrome - FIXED VERSION"""
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Updated headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f'user-agent={self.headers["User-Agent"]}')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # FIXED: Better way to install ChromeDriver
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("✅ Chrome driver initialized successfully")
            return driver
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {e}")
            raise

    def fetch_with_requests(self, url: str) -> str:
        """Fetch page using requests (faster, but may be blocked)"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            random_delay(1, 2)
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def fetch_with_selenium(self, url: str) -> str:
        """Fetch page using Selenium (slower, but more reliable)"""
        driver = None
        try:
            driver = self.setup_driver()
            driver.get(url)
            random_delay(2, 3)
            html = driver.page_source
            logger.info(f"✅ Successfully fetched {url}")
            return html
        except Exception as e:
            logger.error(f"Error with Selenium {url}: {e}")
            return None
        finally:
            if driver:
                driver.quit()

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML with BeautifulSoup"""
        return BeautifulSoup(html, "html.parser")
