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
    ["🏠 Home", "🔍 Scrape Products", "📊 View Database", "📉 Price Tracking", "🤖 AI Analysis", "📈 Reports"]
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
                    
                    # Save to database with NEW upsert logic
                    results = db_manager.save_products_bulk(products)
                    st.success(f"💾 Database Updated:")
                    st.write(f"  ✅ New products: {results['inserted']}")
                    st.write(f"  🔄 Updated products: {results['updated']}")
                    if results['errors'] > 0:
                        st.warning(f"  ⚠️ Errors: {results['errors']}")
                    
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
    
    # Database Statistics at top
    stats = db_manager.get_database_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", stats['total_products'])
    with col2:
        st.metric("Price Drops", stats['price_drops'], delta=f"-{stats['price_drops']}")
    with col3:
        st.metric("Price Increases", stats['price_increases'], delta=f"+{stats['price_increases']}")
    with col4:
        st.metric("Platforms", len(stats['platforms']))
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        platform_filter = st.selectbox(
            "Filter by Platform",
            options=["All"] + stats['platforms']
        )
    
    with col2:
        category_filter = st.selectbox(
            "Filter by Category",
            options=["All"] + stats['categories']
        )
    
    with col3:
        view_mode = st.selectbox(
            "View Mode",
            options=["All Products", "Price Drops Only", "Trending Products"]
        )
    
    # Get products based on filters
    if view_mode == "Price Drops Only":
        products = db_manager.get_price_drops(min_percent=5.0)
    elif view_mode == "Trending Products":
        products = db_manager.get_trending_products(limit=20)
    elif platform_filter == "All":
        products = db_manager.get_all_products(limit=100)
    else:
        products = db_manager.get_products_by_platform(platform_filter)
    
    # Apply category filter
    if category_filter != "All":
        products = [p for p in products if p.get('category') == category_filter]
    
    st.subheader(f"Found {len(products)} Products")
    
    if products:
        # Convert to DataFrame
        df_data = []
        for p in products:
            df_data.append({
                'Title': p.get('title', 'Unknown')[:50] + '...',
                'Platform': p.get('platform', 'N/A').upper(),
                'Current Price': f"₹{p.get('current_price', 0):,.0f}" if p.get('current_price') else "N/A",
                'Rating': f"{p.get('current_rating', 0):.1f}⭐" if p.get('current_rating') else "N/A",
                'Price Trend': p.get('price_trend', 'N/A'),
                'Price Change': f"{p.get('price_change_percent', 0):.1f}%" if p.get('price_change_percent') else "0%",
                'Times Scraped': p.get('times_scraped', 0),
                'Last Seen': p.get('last_seen', 'N/A')
            })
        
        df = pd.DataFrame(df_data)
        
        # Color code price trends
        def color_trend(val):
            if 'down' in str(val).lower():
                return 'background-color: #d4edda'  # Green
            elif 'up' in str(val).lower():
                return 'background-color: #f8d7da'  # Red
            return ''
        
        styled_df = df.style.applymap(color_trend, subset=['Price Trend'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Show detailed view for selected product
        st.markdown("---")
        st.subheader("🔍 Product Details")
        
        product_titles = [p.get('title', 'Unknown')[:50] for p in products[:20]]
        selected_title = st.selectbox("Select a product to view details:", product_titles)
        
        if selected_title:
            selected_product = next(p for p in products if p.get('title', '')[:50] == selected_title)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Product Information**")
                st.write(f"**Title:** {selected_product.get('title', 'N/A')}")
                st.write(f"**Platform:** {selected_product.get('platform', 'N/A').upper()}")
                st.write(f"**Product ID:** {selected_product.get('product_id', 'N/A')}")
                st.write(f"**Category:** {selected_product.get('category', 'N/A')}")
                st.write(f"**Current Price:** ₹{selected_product.get('current_price', 0):,.0f}")
                st.write(f"**Rating:** {selected_product.get('current_rating', 0):.1f}⭐")
                
            with col2:
                st.write("**Tracking Information**")
                st.write(f"**Unique ID:** {selected_product.get('unique_id', 'N/A')}")
                st.write(f"**First Seen:** {selected_product.get('first_seen', 'N/A')}")
                st.write(f"**Last Seen:** {selected_product.get('last_seen', 'N/A')}")
                st.write(f"**Times Scraped:** {selected_product.get('times_scraped', 0)}")
                st.write(f"**Price Trend:** {selected_product.get('price_trend', 'N/A')}")
                st.write(f"**Price Change:** {selected_product.get('price_change_percent', 0):.1f}%")
            
            # Price History Chart
            if selected_product.get('price_history') and len(selected_product['price_history']) > 1:
                st.markdown("---")
                st.write("**📈 Price History**")
                
                price_history = selected_product['price_history']
                history_df = pd.DataFrame(price_history)
                history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
                history_df = history_df.sort_values('timestamp')
                
                st.line_chart(history_df.set_index('timestamp')['price'])
                
                # Show price changes
                st.write("**Price Changes:**")
                for i, entry in enumerate(price_history):
                    st.write(f"  {i+1}. {entry['timestamp']}: ₹{entry['price']:,.0f}")
            
            # Product URL
            if selected_product.get('url'):
                st.markdown(f"[🔗 View on {selected_product.get('platform', 'platform').upper()}]({selected_product['url']})")
        
    else:
        st.info("No products found. Go scrape some data first!")



# ==================== PRICE TRACKING ====================
elif action == "📉 Price Tracking":
    st.header("📉 Price Tracking & Alerts")
    
    tab1, tab2, tab3 = st.tabs(["💰 Price Drops", "📈 Price Increases", "🔔 Alerts"])
    
    with tab1:
        st.subheader("💰 Products with Price Drops")
        
        min_drop = st.slider("Minimum price drop (%)", 0, 50, 10)
        price_drops = db_manager.get_price_drops(min_percent=min_drop)
        
        if price_drops:
            st.metric("Products Found", len(price_drops))
            
            for product in price_drops[:10]:
                with st.expander(f"💵 {product['title'][:60]}... ({product['price_change_percent']:.1f}% off)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Platform:** {product['platform'].upper()}")
                        st.write(f"**Current Price:** ₹{product['current_price']:,.0f}")
                        st.write(f"**Lowest Price:** ₹{product['lowest_price']:,.0f}")
                        st.write(f"**Highest Price:** ₹{product['highest_price']:,.0f}")
                    
                    with col2:
                        st.write(f"**Price Drop:** {product['price_change_percent']:.1f}%")
                        savings = product['highest_price'] - product['current_price']
                        st.write(f"**You Save:** ₹{savings:,.0f}")
                        st.write(f"**Rating:** {product.get('current_rating', 'N/A')}⭐")
                    
                    if product.get('url'):
                        st.markdown(f"[🛒 Buy Now]({product['url']})")
        else:
            st.info(f"No products with >{min_drop}% price drop found.")
    
    with tab2:
        st.subheader("📈 Products with Price Increases")
        
        products = db_manager.get_all_products(limit=100)
        price_increases = [p for p in products if p.get('price_trend') == 'up']
        
        if price_increases:
            st.metric("Products Found", len(price_increases))
            
            for product in sorted(price_increases, key=lambda x: x.get('price_change_percent', 0), reverse=True)[:10]:
                st.write(f"📊 **{product['title'][:60]}...** (+{product['price_change_percent']:.1f}%)")
                st.write(f"   Current: ₹{product['current_price']:,.0f} | Was: ₹{product['lowest_price']:,.0f}")
        else:
            st.info("No price increases detected.")
    
    with tab3:
        st.subheader("🔔 Price Alert Settings")
        st.info("🚧 Coming Soon: Set up email alerts for price drops!")
        
        st.write("**Feature Preview:**")
        st.write("- Get notified when prices drop below a threshold")
        st.write("- Daily/Weekly price summary emails")
        st.write("- Custom alerts for specific products")


# ==================== AI ANALYSIS ====================
elif action == "🤖 AI Analysis":
    st.header("🤖 AI-Powered Analysis")
    
    # Choose analysis type
    analysis_type = st.radio(
        "Select Analysis Type",
        ["⚡ Quick Analysis (Single Agent)", "🧠 Deep Analysis (Multi-Agent Crew)"],
        help="Quick: 5 seconds | Deep: 5-6 minutes with detailed insights"
    )
    
    platform = st.selectbox(
        "Select Platform",
        options=["amazon", "flipkart"]
    )
    
    if analysis_type == "⚡ Quick Analysis (Single Agent)":
        # EXISTING SINGLE AGENT CODE
        if st.button("🧠 Generate Quick Analysis", type="primary"):
            products = db_manager.get_products_by_platform(platform)
            
            if products:
                with st.spinner("🤖 AI is analyzing your products..."):
                    analysis = agent.analyze_products(products)
                    
                    if 'error' not in analysis:
                        st.success("✅ Analysis Complete!")
                        
                        # Display analysis (keep existing code)
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Total Products", analysis.get('total_products', 'N/A'))
                        
                        with col2:
                            price_range = analysis.get('price_range', {})
                            st.metric("Avg Price", f"₹{price_range.get('average', 0):,.0f}")
                        
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
                        
                        # PDF Download
                        st.subheader("📥 Download Report")
                        pdf_bytes = pdf_gen.generate_analysis_report(analysis, platform.upper())
                        st.download_button(
                            label="📄 Download PDF Report",
                            data=pdf_bytes,
                            file_name=f"quick_analysis_{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            type="primary"
                        )
                        
                        # Save report
                        report_data = {
                            'report_type': 'single_agent_analysis',
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
    
    else:  # Deep Analysis with CrewAI
        # NEW CREWAI INTEGRATION
        if st.button("🧠 Generate Deep Analysis (Multi-Agent)", type="primary"):
            products = db_manager.get_products_by_platform(platform)
            
            if products:
                st.info("⏱️ This will take 5-6 minutes. CrewAI agents are working sequentially to avoid rate limits.")
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Import crew manager
                from src.agents.crew_manager import crew_manager
                
                status_text.text("🚀 Starting multi-agent analysis...")
                progress_bar.progress(10)
                
                # Run CrewAI analysis
                with st.spinner("🤖 5 AI Agents are collaborating..."):
                    result = crew_manager.analyze_products(products)
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                if 'error' not in result:
                    st.success("✅ Deep Analysis Complete!")
                    
                    # Show final report
                    st.subheader("📊 Executive Report")
                    st.write(result.get('final_report', 'No report generated'))
                    
                    # Show detailed results from each agent
                    st.markdown("---")
                    st.subheader("🔍 Detailed Agent Outputs")
                    
                    for agent_result in result.get('detailed_results', []):
                        with st.expander(f"🤖 {agent_result['agent']}"):
                            st.write(agent_result['output'])
                    
                    st.markdown("---")
                    st.metric("Tasks Completed", result.get('tasks_completed', 0))
                    
                    # Save CrewAI report
                    report_data = {
                        'report_type': 'crew_ai_analysis',
                        'platform': platform,
                        'analysis': result,
                        'products_analyzed': len(products)
                    }
                    report_id = db_manager.save_report(report_data)
                    st.success(f"💾 Report saved to database (ID: {report_id})")
                    
                else:
                    st.error(f"❌ Error: {result['error']}")
                    st.info("💡 Tip: If you hit rate limits, wait a few minutes and try again.")
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