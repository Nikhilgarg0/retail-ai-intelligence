# src/ui/dashboard.py
import streamlit as st
from src.scrapers.amazon_scraper import AmazonScraper
from src.database.mongo_manager import db_manager
from src.agents.analysis_agent import ProductAnalysisAgent
import pandas as pd
import json
from src.utils.pdf_generator import ReportPDFGenerator
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Retail Intelligence System",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 AI Retail Intelligence System")
st.markdown("**Scrape, Analyze, and Get Insights from E-commerce Data**")

# Sidebar
st.sidebar.header("⚙️ Controls")
action = st.sidebar.selectbox(
    "Choose Action",
    ["🏠 Home", "🔍 Scrape Products", "📊 View Database", "🤖 AI Analysis", "📈 Reports"]
)

# Initialize components
@st.cache_resource
def get_scraper():
    return AmazonScraper()

@st.cache_resource
def get_agent():
    return ProductAnalysisAgent()

scraper = get_scraper()
agent = get_agent()

pdf_gen = ReportPDFGenerator()

# ==================== HOME ====================
if action == "🏠 Home":
    st.header("Welcome to Your Retail Intelligence System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_products = db_manager.products.count_documents({})
        st.metric("📦 Total Products", total_products)
    
    with col2:
        total_reports = db_manager.reports.count_documents({})
        st.metric("📋 Reports Generated", total_reports)
    
    with col3:
        st.metric("🏪 Platforms", "1 (Amazon)")
    
    st.markdown("---")
    st.subheader("🚀 Quick Start Guide")
    st.markdown("""
    1. **🔍 Scrape Products** - Search Amazon and collect product data
    2. **📊 View Database** - See all scraped products
    3. **🤖 AI Analysis** - Get AI-powered insights on your data
    4. **📈 Reports** - View historical analysis reports
    """)

# ==================== SCRAPE PRODUCTS ====================
elif action == "🔍 Scrape Products":
    st.header("🔍 Scrape Amazon Products")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search Query",
            placeholder="e.g., wireless headphones, samsung phone, laptop"
        )
    
    with col2:
        max_results = st.number_input("Max Products", min_value=1, max_value=20, value=5)
    
    if st.button("🚀 Start Scraping", type="primary"):
        if search_query:
            with st.spinner(f"Scraping Amazon for '{search_query}'..."):
                products = scraper.search_products(search_query, max_results=max_results)
                
                if products:
                    st.success(f"✅ Found {len(products)} products!")
                    
                    # Add category
                    for product in products:
                        product['category'] = 'electronics'
                    
                    # Save to database
                    ids = db_manager.save_products_bulk(products)
                    st.info(f"💾 Saved {len(ids)} products to database")
                    
                    # Display results
                    st.subheader("Scraped Products")
                    df = pd.DataFrame(products)
                    df = df[['title', 'price', 'rating', 'reviews', 'platform']]
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error("❌ No products found. Try a different search term.")
        else:
            st.warning("⚠️ Please enter a search query")

# ==================== VIEW DATABASE ====================
elif action == "📊 View Database":
    st.header("📊 Database Explorer")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        platform_filter = st.selectbox(
            "Filter by Platform",
            options=["All", "amazon", "flipkart"]
        )
    
    with col2:
        category_filter = st.selectbox(
            "Filter by Category",
            options=["All", "electronics", "clothing", "groceries"]
        )
    
    # Get products
    if platform_filter == "All":
        products = list(db_manager.products.find())
    else:
        products = db_manager.get_products_by_platform(platform_filter)
    
    if category_filter != "All":
        products = [p for p in products if p.get('category') == category_filter]
    
    st.metric("Total Products", len(products))
    
    if products:
        # Convert to DataFrame
        df = pd.DataFrame(products)
        
        # Clean up for display
        display_columns = ['title', 'price', 'rating', 'reviews', 'platform', 'category']
        display_columns = [col for col in display_columns if col in df.columns]
        
        st.dataframe(df[display_columns], use_container_width=True)
        
        # Price distribution
        if 'price' in df.columns:
            st.subheader("💰 Price Distribution")
            price_data = df['price'].dropna()
            if len(price_data) > 0:
                st.bar_chart(price_data)
    else:
        st.info("No products found. Go scrape some data first!")

# ==================== AI ANALYSIS ====================
elif action == "🤖 AI Analysis":
    st.header("🤖 AI-Powered Analysis")
    
    platform = st.selectbox(
        "Select Platform",
        options=["amazon", "flipkart"]
    )
    
    if st.button("🧠 Generate Analysis", type="primary"):
        products = db_manager.get_products_by_platform(platform)
        
        if products:
            with st.spinner("🤖 AI is analyzing your products..."):
                analysis = agent.analyze_products(products)
                
                if 'error' not in analysis:
                    st.success("✅ Analysis Complete!")
                    
                    # Display analysis
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Total Products",
                            analysis.get('total_products', 'N/A')
                        )
                    
                    with col2:
                        price_range = analysis.get('price_range', {})
                        st.metric(
                            "Avg Price",
                            f"₹{price_range.get('average', 0):,.0f}"
                        )
                    
                    with col3:
                        st.metric(
                            "Price Range",
                            f"₹{price_range.get('min', 0):,.0f} - ₹{price_range.get('max', 0):,.0f}"
                        )
                    
                    st.markdown("---")
                    
                    # Top rated product
                    st.subheader("🏆 Top Rated Product")
                    top_product = analysis.get('top_rated_product', {})
                    if top_product:
                        st.write(f"**{top_product.get('title', 'N/A')}**")
                        st.write(f"Rating: {top_product.get('rating', 'N/A')} ⭐ | Price: ₹{top_product.get('price', 0):,.0f}")
                    
                    # Best value
                    st.subheader("💎 Best Value Product")
                    best_value = analysis.get('best_value_product', {})
                    if best_value:
                        st.write(f"**{best_value.get('title', 'N/A')}**")
                        st.write(best_value.get('reason', 'N/A'))
                    
                    # Insights
                    st.subheader("💡 Price Insights")
                    insights = analysis.get('price_insights', [])
                    for insight in insights:
                        st.write(f"• {insight}")
                    
                    # Recommendations
                    st.subheader("📋 Recommendations")
                    recommendations = analysis.get('recommendations', [])
                    for rec in recommendations:
                        st.write(f"✓ {rec}")
                    
                    st.markdown("---")
                    
                    # 🆕 PDF DOWNLOAD BUTTON
                    st.subheader("📥 Download Report")
                    
                    # Generate PDF
                    pdf_bytes = pdf_gen.generate_analysis_report(analysis, platform.upper())
                    
                    # Create download button
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"retail_analysis_{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
                    
                    # Save report
                    report_data = {
                        'report_type': 'product_analysis',
                        'platform': platform,
                        'analysis': analysis,
                        'products_analyzed': len(products)
                    }
                    report_id = db_manager.save_report(report_data)
                    st.success(f"💾 Report saved to database (ID: {report_id})")
                else:
                    st.error(f"❌ Error: {analysis['error']}")
        else:
            st.warning("⚠️ No products found for this platform. Scrape some data first!")

# ==================== REPORTS ====================
elif action == "📈 Reports":
    st.header("📈 Historical Reports")
    
    reports = list(db_manager.reports.find().sort('generated_at', -1))
    
    if reports:
        st.metric("Total Reports", len(reports))
        
        for i, report in enumerate(reports[:10]):
            report_date = report.get('generated_at', 'N/A')
            with st.expander(f"Report {i+1} - {report.get('report_type', 'Unknown')} ({report_date})"):
                st.json(report.get('analysis', {}))
    else:
        st.info("No reports yet. Run an AI analysis to generate your first report!")

# Footer
st.markdown("---")
st.markdown("**Built with Streamlit, Selenium, MongoDB, and Gemini AI** | 🚀 Retail Intelligence System")