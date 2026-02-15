# debug_flipkart.py
from src.scrapers.base_scraper import BaseScraper

print("Debugging Flipkart HTML structure...\n")

scraper = BaseScraper()
url = "https://www.flipkart.com/search?q=wireless+headphones"

print("Fetching Flipkart search page...")
html = scraper.fetch_with_selenium(url)

if html:
    soup = scraper.parse_html(html)
    
    # Try to find product containers
    # Flipkart uses different classes than Amazon
    possible_containers = [
        soup.find_all('div', {'class': '_1AtVbE'}),  # Common product card class
        soup.find_all('div', {'data-id': True}),     # Products with data-id
        soup.find_all('div', class_='_4ddWXP'),      # Another common class
        soup.find_all('a', class_='_1fQZEK'),        # Product links
    ]
    
    print(f"Testing different selectors:")
    for i, containers in enumerate(possible_containers, 1):
        print(f"  Selector {i}: Found {len(containers)} elements")
    
    # Show first product structure if found
    for containers in possible_containers:
        if containers and len(containers) > 0:
            print(f"\n{'='*60}")
            print("FIRST PRODUCT HTML STRUCTURE:")
            print(f"{'='*60}")
            print(containers[0].prettify()[:2000])
            break
    
else:
    print("❌ Failed to fetch page")