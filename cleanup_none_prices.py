# cleanup_none_prices.py
from src.database.mongo_manager import db_manager

print("Cleaning up products with None prices...\n")

# Find products with None prices
products_with_none = list(db_manager.products.find({'current_price': None}))

print(f"Found {len(products_with_none)} products with None prices")

if products_with_none:
    # Delete them
    result = db_manager.products.delete_many({'current_price': None})
    print(f"✅ Deleted {result.deleted_count} products")
else:
    print("✅ No cleanup needed!")

# Show stats
stats = db_manager.get_database_stats()
print(f"\n📊 Database after cleanup:")
print(f"   Total Products: {stats['total_products']}")
print(f"   Platforms: {stats['platforms']}")