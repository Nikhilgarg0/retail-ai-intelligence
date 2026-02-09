# debug_flipkart.py
from src.scrapers.base_scraper import BaseScraper

print("Debugging Flipkart HTML structure...\n")

scraper = BaseScraper()
url = "https://www.flipkart.com/search?q=wireless+headphones"

print("Fetching Flipkart page...")
html = scraper.fetch_with_selenium(url)

if html:
    soup = scraper.parse_html(html)
    
    # Try to find product containers
    # Flipkart uses different class names than Amazon
    
    # Check for common Flipkart product div classes
    possible_classes = [
        'tUxRFH',  # Common product card class
        '_1AtVbE',
        '_2kHMtA',
        'cPHDOP',
        'slAVV4'
    ]
    
    print("Looking for product containers...\n")
    
    for class_name in possible_classes:
        divs = soup.find_all('div', class_=class_name)
        if divs:
            print(f"✅ Found {len(divs)} elements with class '{class_name}'")
    
    # Try finding by data attributes
    products = soup.find_all('div', {'data-id': True})
    print(f"\n✅ Found {len(products)} products with data-id attribute")
    
    if products:
        print("\n" + "="*60)
        print("FIRST PRODUCT HTML:")
        print("="*60)
        print(products[0].prettify()[:2000])
        
        # Try to find title
        print("\n" + "="*60)
        print("Looking for TITLE:")
        title = products[0].find('a', class_='wjcEIp')
        if title:
            print(f"✅ Found: {title.get_text(strip=True)[:80]}")
        
        title2 = products[0].find('div', class_='KzDlHZ')
        if title2:
            print(f"✅ Found alternative: {title2.get_text(strip=True)[:80]}")
        
        # Try to find price
        print("\nLooking for PRICE:")
        price = products[0].find('div', class_='Nx9bqj')
        if price:
            print(f"✅ Found: {price.get_text(strip=True)}")
        
        # Try to find rating
        print("\nLooking for RATING:")
        rating = products[0].find('div', class_='XQDdHH')
        if rating:
            print(f"✅ Found: {rating.get_text(strip=True)}")
    
    else:
        print("❌ No products found with data-id")
        print("\nShowing first 3000 characters of HTML:")
        print(html[:3000])
else:
    print("❌ Failed to fetch page")