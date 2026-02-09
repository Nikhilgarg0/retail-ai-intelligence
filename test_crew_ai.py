# test_crew_ai.py
import os
from config.settings import settings  # Correct path: config/settings.py
from src.database.mongo_manager import db_manager
from src.agents.crew_manager import crew_manager
import json

# Set Groq API key as environment variable for CrewAI
os.environ['GROQ_API_KEY'] = settings.groq_api_key

print("Testing CrewAI Multi-Agent System...\n")
print("=" * 60)

# Get products from database
print("📊 Fetching products from MongoDB...")
products = db_manager.get_products_by_platform('amazon')

if not products:
    print("❌ No products found! Run the scraper first.")
    print("   Command: python test_amazon_scraper.py")
    exit()

print(f"✅ Found {len(products)} products\n")
print("=" * 60)

# Run CrewAI analysis
print("\n🤖 Starting CrewAI Multi-Agent Analysis...")
print("   This will take 30-60 seconds...\n")
print("=" * 60)

result = crew_manager.analyze_products(products)

print("\n" + "=" * 60)
print("📈 CREWAI ANALYSIS RESULTS")
print("=" * 60)
print(json.dumps(result, indent=2))
print("=" * 60)

# Save to database
print("\n💾 Saving CrewAI report to database...")
report_data = {
    'report_type': 'crew_ai_analysis',
    'platform': 'amazon',
    'analysis': result,
    'products_analyzed': len(products)
}

report_id = db_manager.save_report(report_data)
print(f"✅ Report saved with ID: {report_id}")

print("\n🎉 CrewAI test complete!")