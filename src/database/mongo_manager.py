from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBManager:
    """Manages all MongoDB operations for retail intelligence"""
    
    def __init__(self):
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client['retail_intelligence']
        
        # Collections
        self.products = self.db['products']  # Raw scraped product data
        self.price_history = self.db['price_history']  # Price tracking over time
        self.competitors = self.db['competitors']  # Competitor analysis
        self.reports = self.db['reports']  # AI-generated reports
        
        logger.info("✅ MongoDB Manager initialized")
    
    def save_product(self, product_data: Dict) -> str:
        """Save a scraped product to database"""
        product_data['scraped_at'] = datetime.now()
        product_data['updated_at'] = datetime.now()
        
        result = self.products.insert_one(product_data)
        logger.info(f"Saved product: {product_data.get('title', 'Unknown')[:50]}")
        return str(result.inserted_id)
    
    def save_products_bulk(self, products: List[Dict]) -> List[str]:
        """Save multiple products at once"""
        for product in products:
            product['scraped_at'] = datetime.now()
            product['updated_at'] = datetime.now()
        
        result = self.products.insert_many(products)
        logger.info(f"Saved {len(products)} products")
        return [str(id) for id in result.inserted_ids]
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """Get all products in a category"""
        products = list(self.products.find({'category': category}))
        return products
    
    def get_products_by_platform(self, platform: str) -> List[Dict]:
        """Get all products from a platform (amazon, flipkart, etc.)"""
        products = list(self.products.find({'platform': platform}))
        return products
    
    def save_price_history(self, product_id: str, price: float, platform: str):
        """Track price changes over time"""
        price_record = {
            'product_id': product_id,
            'platform': platform,
            'price': price,
            'recorded_at': datetime.now()
        }
        self.price_history.insert_one(price_record)
    
    def get_price_trends(self, product_id: str) -> List[Dict]:
        """Get price history for a product"""
        history = list(self.price_history.find(
            {'product_id': product_id}
        ).sort('recorded_at', -1))
        return history
    
    def save_report(self, report_data: Dict) -> str:
        """Save AI-generated analysis report"""
        report_data['generated_at'] = datetime.now()
        result = self.reports.insert_one(report_data)
        logger.info("Report saved to database")
        return str(result.inserted_id)
    
    def get_latest_report(self, report_type: str = None) -> Optional[Dict]:
        """Get the most recent report"""
        query = {'report_type': report_type} if report_type else {}
        report = self.reports.find_one(query, sort=[('generated_at', -1)])
        return report
    
    def close(self):
        """Close database connection"""
        self.client.close()
        logger.info("MongoDB connection closed")

# Global instance
db_manager = MongoDBManager()