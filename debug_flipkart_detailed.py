# debug_flipkart_detailed.py
from src.scrapers.base_scraper import BaseScraper

print("Detailed Flipkart Product Analysis...\n")

scraper = BaseScraper()
url = "https://www.flipkart.com/search?q=wireless+headphones"

html = scraper.fetch_with_selenium(url)

if html:
    soup = scraper.parse_html(html)
    
    # Find products
    products = soup.find_all('div', {'data-id': True})
    
    if products:
        print(f"Found {len(products)} products\n")
        print("=" * 60)
        print("ANALYZING FIRST PRODUCT IN DETAIL:")
        print("=" * 60)
        
        first = products[0]
        
        # Show full HTML
        print("\n📦 FULL PRODUCT HTML:\n")
        print(first.prettify()[:3000])
        
        print("\n" + "=" * 60)
        print("🔍 SEARCHING FOR PRICE:")
        print("=" * 60)
        
        # Try multiple price selectors
        price_candidates = [
            first.find('div', class_='Nx9bqj'),
            first.find('div', class_='hl05eU'),
            first.find('div', class_='Nx9bqj CxhGGd'),
            first.find('div', string=lambda text: '₹' in str(text) if text else False),
            first.find_all(string=lambda text: '₹' in str(text) if text else False)
        ]
        
        for i, candidate in enumerate(price_candidates, 1):
            if candidate:
                print(f"\nPrice Candidate {i}: {candidate}")
        
        print("\n" + "=" * 60)
        print("⭐ SEARCHING FOR RATING:")
        print("=" * 60)
        
        # Try multiple rating selectors
        rating_candidates = [
            first.find('div', class_='XQDdHH'),
            first.find('span', class_='XQDdHH'),
            first.find('div', class_='Wphh3N'),
            first.find_all(string=lambda text: any(c.isdigit() and '.' in str(text) for c in str(text)))
        ]
        
        for i, candidate in enumerate(rating_candidates, 1):
            if candidate:
                print(f"\nRating Candidate {i}: {candidate}")
        
        print("\n" + "=" * 60)
        print("🏷️ ALL DIVS WITH TEXT CONTAINING ₹:")
        print("=" * 60)
        
        all_divs = first.find_all('div')
        for div in all_divs:
            text = div.get_text(strip=True)
            if '₹' in text and len(text) < 30:  # Short text with rupee symbol
                print(f"  Class: {div.get('class')} | Text: {text}")