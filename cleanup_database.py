# cleanup_database.py
from pymongo import MongoClient
from config.settings import settings

print("🧹 Database Cleanup Tool\n")
print("=" * 60)

# Connect to MongoDB
client = MongoClient(settings.mongodb_uri)
db = client['retail_intelligence']

# Get current counts
products_count = db.products.count_documents({})
reports_count = db.reports.count_documents({})

print(f"📊 Current Database Status:")
print(f"   Products: {products_count}")
print(f"   Reports: {reports_count}\n")

# Confirm deletion
print("⚠️  WARNING: This will delete ALL products!")
print("   Reports will be kept.")
print()
response = input("Type 'DELETE' to confirm: ")

if response == "DELETE":
    # Drop the products collection (removes all data and indexes)
    db.products.drop()
    print("✅ Products collection dropped")
    
    # Recreate empty collection
    db.create_collection('products')
    print("✅ Fresh products collection created")
    
    print("\n🎉 Database cleaned! Ready for new schema.")
else:
    print("\n❌ Cleanup cancelled")

client.close()