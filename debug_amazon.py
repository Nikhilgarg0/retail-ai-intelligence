# debug_amazon.py
from src.scrapers.base_scraper import BaseScraper

print("Debugging Amazon HTML structure...\n")

scraper = BaseScraper()
url = "https://www.amazon.in/s?k=wireless+headphones"

print("Fetching page...")
html = scraper.fetch_with_selenium(url)

if html:
    soup = scraper.parse_html(html)
    
    # Find product containers
    product_divs = soup.find_all('div', {'data-component-type': 's-search-result'})
    print(f"Found {len(product_divs)} product divs\n")
    
    if product_divs:
        # Look at the FIRST product in detail
        first_product = product_divs[0]
        
        print("="*60)
        print("FIRST PRODUCT HTML STRUCTURE:")
        print("="*60)
        print(first_product.prettify()[:2000])  # First 2000 characters
        print("\n" + "="*60)
        
        # Try to find title in different ways
        print("\nLooking for TITLE:")
        title_h2 = first_product.find('h2')
        if title_h2:
            print(f"  ✅ Found h2: {title_h2.get_text(strip=True)[:80]}")
        
        title_span = first_product.find('span', class_='a-size-medium')
        if title_span:
            print(f"  ✅ Found span.a-size-medium: {title_span.get_text(strip=True)[:80]}")
        
        # Look for price
        print("\nLooking for PRICE:")
        price_whole = first_product.find('span', class_='a-price-whole')
        if price_whole:
            print(f"  ✅ Found price-whole: {price_whole.get_text(strip=True)}")
        else:
            # Try alternative
            price_symbol = first_product.find('span', class_='a-price-symbol')
            if price_symbol:
                print(f"  ✅ Found price-symbol: {price_symbol.get_text(strip=True)}")
        
        # Look for rating
        print("\nLooking for RATING:")
        rating = first_product.find('span', class_='a-icon-alt')
        if rating:
            print(f"  ✅ Found rating: {rating.get_text(strip=True)}")
        
        # Look for ASIN
        print("\nLooking for ASIN:")
        asin = first_product.get('data-asin')
        print(f"  ASIN: {asin}")
        
    else:
        print("❌ No products found!")
else:
    print("❌ Failed to fetch page")