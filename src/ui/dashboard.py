# src/ui/dashboard.py
import streamlit as st
from src.scrapers.amazon_scraper import AmazonScraper
from src.scrapers.flipkart_scraper import FlipkartScraper
from src.database.mongo_manager import db_manager
from src.agents.analysis_agent import ProductAnalysisAgent
from src.utils.pdf_generator import ReportPDFGenerator
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Retail Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional look
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f9fafb;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Initialize components
@st.cache_resource
def get_scrapers():
    return {"amazon": AmazonScraper(), "flipkart": FlipkartScraper()}


@st.cache_resource
def get_agent():
    return ProductAnalysisAgent()


@st.cache_resource
def get_pdf_gen():
    return ReportPDFGenerator()


scrapers = get_scrapers()
agent = get_agent()
pdf_gen = get_pdf_gen()

# Sidebar Navigation
with st.sidebar:
    st.title("Navigation")

    page = st.radio(
        "Navigate",
        [
            "Dashboard",
            "Data Collection",
            "Product Explorer",
            "Price Analytics",
            "AI Insights",
            "Reports",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    # Database stats in sidebar
    stats = db_manager.get_database_stats()
    st.subheader("System Status")
    st.metric("Total Products", stats["total_products"])
    st.metric("Active Platforms", len(stats["platforms"]))
    st.metric("Reports Generated", stats["total_reports"])

# Main content area
if page == "Dashboard":
    st.markdown(
        '<p class="main-header">Retail Intelligence Platform</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-header">Real-time competitive intelligence and market analysis</p>',
        unsafe_allow_html=True,
    )

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Products Tracked",
            value=stats["total_products"],
            delta="Active monitoring",
        )

    with col2:
        st.metric(
            label="Price Drops Detected",
            value=stats["price_drops"],
            delta=f"-{stats['price_drops']} opportunities",
        )

    with col3:
        st.metric(
            label="Price Increases",
            value=stats["price_increases"],
            delta=f"+{stats['price_increases']} trends",
        )

    with col4:
        st.metric(
            label="Platforms Monitored",
            value=len(stats["platforms"]),
            delta="Multi-platform",
        )

    st.divider()

    # Quick actions
    st.subheader("Quick Actions")
    st.markdown("""
    Use the sidebar navigation to:
    - **Data Collection** - Scrape products from Amazon and Flipkart
    - **Product Explorer** - Browse and analyze collected data
    - **Price Analytics** - Track price changes and opportunities
    - **AI Insights** - Generate intelligent market analysis
    - **Reports** - View historical analysis reports
    """)

    st.divider()

    # Recent activity
    st.subheader("Recent Activity")

    # Get recent products
    recent_products = db_manager.get_all_products(limit=10)

    if recent_products:
        activity_data = []
        for p in recent_products:
            activity_data.append(
                {
                    "Platform": p.get("platform", "N/A").upper(),
                    "Product": p.get("title", "Unknown")[:60] + "...",
                    "Current Price": (
                        f"₹{p.get('current_price', 0):,.0f}"
                        if p.get("current_price")
                        else "N/A"
                    ),
                    "Trend": p.get("price_trend", "stable").capitalize(),
                    "Last Updated": p.get("last_seen", "N/A"),
                }
            )

        df = pd.DataFrame(activity_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No activity yet. Start by collecting data from e-commerce platforms.")

elif page == "Data Collection":
    st.header("Data Collection")
    st.markdown("Scrape product data from e-commerce platforms")

    # Configuration
    col1, col2 = st.columns([3, 1])

    with col1:
        search_query = st.text_input(
            "Search Query",
            placeholder="Enter product name or category",
            help="Example: wireless headphones, laptop, smartphone",
        )

    with col2:
        max_results = st.number_input(
            "Maximum Results",
            min_value=1,
            max_value=50,
            value=10,
            help="Number of products to scrape",
        )

    # Platform and category selection
    col1, col2 = st.columns(2)

    with col1:
        platform = st.selectbox(
            "Platform",
            options=["Amazon", "Flipkart"],
            help="Select e-commerce platform",
        )

    with col2:
        category = st.selectbox(
            "Category",
            options=[
                "Electronics",
                "Clothing",
                "Cosmetics",
                "Groceries",
                "Home & Kitchen",
            ],
            help="Product category for better organization",
        )

    # Scrape button
    if st.button("Start Collection", type="primary", use_container_width=True):
        if search_query:
            scraper = scrapers[platform.lower()]

            with st.spinner(f"Collecting data from {platform}..."):
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("Initializing scraper...")
                progress_bar.progress(20)

                products = scraper.search_products(
                    search_query, max_results=max_results
                )
                progress_bar.progress(60)

                if products:
                    status_text.text("Processing results...")

                    # Add category
                    for product in products:
                        product["category"] = category.lower()

                    # Save to database
                    results = db_manager.save_products_bulk(products)
                    progress_bar.progress(100)

                    status_text.empty()
                    progress_bar.empty()

                    # Results summary
                    st.success(
                        f"Collection completed: {len(products)} products processed"
                    )

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("New Products", results["inserted"])
                    with col2:
                        st.metric("Updated Products", results["updated"])
                    with col3:
                        st.metric("Errors", results["errors"])

                    # Display results
                    st.subheader("Collected Products")

                    df_data = []
                    for p in products:
                        df_data.append(
                            {
                                "Title": p.get("title", "Unknown")[:50] + "...",
                                "Price": (
                                    f"₹{p.get('price'):,.0f}"
                                    if p.get("price")
                                    else "N/A"
                                ),
                                "Rating": (
                                    f"{p.get('rating'):.1f}"
                                    if p.get("rating")
                                    else "N/A"
                                ),
                                "Platform": p.get("platform", "N/A").upper(),
                            }
                        )

                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.error("No products found. Please try a different search query.")
        else:
            st.warning("Please enter a search query")

elif page == "Product Explorer":
    st.header("Product Explorer")
    st.markdown("Browse and analyze collected product data")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        platform_filter = st.selectbox(
            "Platform", options=["All"] + [p.upper() for p in stats["platforms"]]
        )

    with col2:
        category_filter = st.selectbox(
            "Category", options=["All"] + [c.capitalize() for c in stats["categories"]]
        )

    with col3:
        view_mode = st.selectbox(
            "View", options=["All Products", "Price Drops", "Trending"]
        )

    # Get filtered products
    if view_mode == "Price Drops":
        products = db_manager.get_price_drops(min_percent=5.0)
    elif view_mode == "Trending":
        products = db_manager.get_trending_products(limit=50)
    elif platform_filter == "All":
        products = db_manager.get_all_products(limit=100)
    else:
        products = db_manager.get_products_by_platform(platform_filter.lower())

    # Apply filters
    if category_filter != "All":
        products = [
            p
            for p in products
            if p.get("category", "").lower() == category_filter.lower()
        ]

    st.subheader(f"Results: {len(products)} products")

    if products:
        # Create display dataframe
        df_data = []
        for p in products:
            df_data.append(
                {
                    "Product": p.get("title", "Unknown")[:60] + "...",
                    "Platform": p.get("platform", "N/A").upper(),
                    "Price": (
                        f"₹{p.get('current_price', 0):,.0f}"
                        if p.get("current_price")
                        else "N/A"
                    ),
                    "Rating": (
                        f"{p.get('current_rating', 0):.1f}"
                        if p.get("current_rating")
                        else "N/A"
                    ),
                    "Trend": p.get("price_trend", "stable").capitalize(),
                    "Change": (
                        f"{p.get('price_change_percent', 0):.1f}%"
                        if p.get("price_change_percent")
                        else "0%"
                    ),
                    "Scraped": p.get("times_scraped", 0),
                }
            )

        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Detailed view
        st.divider()
        st.subheader("Product Details")

        selected_idx = st.selectbox(
            "Select product for details",
            options=range(len(products)),
            format_func=lambda x: products[x].get("title", "Unknown")[:60] + "...",
        )

        if selected_idx is not None:
            product = products[selected_idx]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Product Information**")
                st.write(f"**Title:** {product.get('title')}")
                st.write(f"**Platform:** {product.get('platform', 'N/A').upper()}")
                st.write(f"**Category:** {product.get('category', 'N/A').capitalize()}")
                st.write(f"**Product ID:** {product.get('product_id')}")
                st.write(f"**Price:** ₹{product.get('current_price', 0):,.0f}")
                st.write(f"**Rating:** {product.get('current_rating', 'N/A')}")

            with col2:
                st.markdown("**Tracking Data**")
                st.write(f"**First Seen:** {product.get('first_seen')}")
                st.write(f"**Last Updated:** {product.get('last_seen')}")
                st.write(f"**Times Scraped:** {product.get('times_scraped', 0)}")
                st.write(
                    f"**Price Trend:** {product.get('price_trend', 'N/A').capitalize()}"
                )
                st.write(
                    f"**Price Change:** {product.get('price_change_percent', 0):.1f}%"
                )

            # Price history chart
            if product.get("price_history") and len(product["price_history"]) > 1:
                st.divider()
                st.markdown("**Price History**")

                history_df = pd.DataFrame(product["price_history"])
                history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])
                history_df = history_df.sort_values("timestamp")

                st.line_chart(
                    history_df.set_index("timestamp")["price"], use_container_width=True
                )
    else:
        st.info("No products found matching the selected filters.")

elif page == "Price Analytics":
    st.header("Price Analytics")
    st.markdown("Track price changes and identify opportunities")

    tab1, tab2, tab3 = st.tabs(["Price Drops", "Price Increases", "Price Distribution"])

    with tab1:
        st.subheader("Products with Price Reductions")

        min_drop = st.slider("Minimum price drop percentage", 0, 50, 10)
        price_drops = db_manager.get_price_drops(min_percent=min_drop)

        if price_drops:
            st.metric("Opportunities Found", len(price_drops))

            for product in price_drops[:20]:
                with st.expander(
                    f"{product['title'][:70]}... ({product['price_change_percent']:.1f}% off)"
                ):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Platform:** {product['platform'].upper()}")
                        st.write(f"**Current Price:** ₹{product['current_price']:,.0f}")
                        st.write(
                            f"**Previous Price:** ₹{product['highest_price']:,.0f}"
                        )

                    with col2:
                        savings = product["highest_price"] - product["current_price"]
                        st.write(
                            f"**Discount:** {product['price_change_percent']:.1f}%"
                        )
                        st.write(f"**Savings:** ₹{savings:,.0f}")
                        st.write(f"**Rating:** {product.get('current_rating', 'N/A')}")

                    if product.get("url"):
                        st.link_button("View Product", product["url"])
        else:
            st.info(f"No products found with >{min_drop}% price drop.")

    with tab2:
        st.subheader("Products with Price Increases")

        products = db_manager.get_all_products(limit=100)
        price_increases = [p for p in products if p.get("price_trend") == "up"]

        if price_increases:
            st.metric("Products Found", len(price_increases))

            df_data = []
            for p in sorted(
                price_increases,
                key=lambda x: x.get("price_change_percent", 0),
                reverse=True,
            )[:20]:
                df_data.append(
                    {
                        "Product": p["title"][:60] + "...",
                        "Platform": p["platform"].upper(),
                        "Current": f"₹{p['current_price']:,.0f}",
                        "Previous": f"₹{p['lowest_price']:,.0f}",
                        "Change": f"+{p['price_change_percent']:.1f}%",
                    }
                )

            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No price increases detected.")

    with tab3:
        st.subheader("Price Distribution Analysis")

        all_products = db_manager.get_all_products(limit=100)

        if all_products:
            prices = [
                p["current_price"] for p in all_products if p.get("current_price")
            ]

            if prices:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Average Price", f"₹{sum(prices)/len(prices):,.0f}")
                with col2:
                    st.metric("Minimum Price", f"₹{min(prices):,.0f}")
                with col3:
                    st.metric("Maximum Price", f"₹{max(prices):,.0f}")

                # Price distribution chart
                st.bar_chart(pd.Series(prices), use_container_width=True)


elif page == "AI Insights":
    st.header("AI-Powered Analysis")
    st.markdown("Generate intelligent insights from collected data")
    
    # Initialize session state for storing analysis results
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    if 'analysis_platform' not in st.session_state:
        st.session_state.analysis_platform = None
    
    # Analysis configuration
    col1, col2 = st.columns([3, 1])
    
    with col1:
        analysis_type = st.radio(
            "Analysis Type",
            ["Quick Analysis", "Deep Analysis (Multi-Agent)"],
            help="Quick: 5-10 seconds | Deep: 5-6 minutes with detailed insights"
        )
    
    with col2:
        platform = st.selectbox(
            "Select Platform",
            options=["amazon", "flipkart"]
        )
    
    # Start New Analysis Button
    if st.button("🔄 Start New Analysis", type="primary", use_container_width=True):
        products = db_manager.get_products_by_platform(platform)
        
        if products:
            if analysis_type == "Quick Analysis":
                with st.spinner("Analyzing product data..."):
                    analysis = agent.analyze_products(products)
                    
                    if 'error' not in analysis:
                        st.session_state.current_analysis = analysis
                        st.session_state.analysis_platform = platform
                        st.session_state.analysis_type = 'quick'
                        
                        # Save report
                        report_data = {
                            'report_type': 'quick_analysis',
                            'platform': platform,
                            'analysis': analysis,
                            'products_analyzed': len(products)
                        }
                        report_id = db_manager.save_report(report_data)
                        st.session_state.last_report_id = str(report_id)
                        
                        st.rerun()
                    else:
                        st.error(f"Analysis failed: {analysis['error']}")
            
            else:  # Deep Analysis
                st.info("Deep analysis will take 5-6 minutes to complete.")
                
                from src.agents.crew_manager import crew_manager
                
                with st.spinner("Multi-agent analysis in progress..."):
                    result = crew_manager.analyze_products(products)
                
                if 'error' not in result:
                    st.session_state.current_analysis = result
                    st.session_state.analysis_platform = platform
                    st.session_state.analysis_type = 'deep'
                    
                    # Save report
                    report_data = {
                        'report_type': 'deep_analysis',
                        'platform': platform,
                        'analysis': result,
                        'products_analyzed': len(products)
                    }
                    report_id = db_manager.save_report(report_data)
                    st.session_state.last_report_id = str(report_id)
                    
                    st.rerun()
                else:
                    st.error(f"Analysis failed: {result['error']}")
        else:
            st.warning("No products found for this platform. Please collect data first.")
    
    # Display current analysis if exists
    if st.session_state.current_analysis is not None:
        st.divider()
        st.success("✅ Analysis completed successfully")
        
        analysis = st.session_state.current_analysis
        analysis_type_label = st.session_state.get('analysis_type', 'quick')
        
        if analysis_type_label == 'quick':
            # Display Quick Analysis
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Products Analyzed", analysis.get('total_products', 0))
            
            with col2:
                price_range = analysis.get('price_range', {})
                st.metric("Average Price", f"₹{price_range.get('average', 0):,.0f}")
            
            with col3:
                st.metric(
                    "Price Range",
                    f"₹{price_range.get('min', 0):,.0f} - ₹{price_range.get('max', 0):,.0f}"
                )
            
            st.divider()
            
            # Top rated product
            st.subheader("Top Rated Product")
            top_product = analysis.get('top_rated_product', {})
            if top_product:
                st.write(f"**{top_product.get('title', 'N/A')}**")
                st.write(f"Rating: {top_product.get('rating', 'N/A')} | Price: ₹{top_product.get('price', 0):,.0f}")
            
            # Best value
            st.subheader("Best Value Product")
            best_value = analysis.get('best_value_product', {})
            if best_value:
                st.write(f"**{best_value.get('title', 'N/A')}**")
                st.write(best_value.get('reason', 'N/A'))
            
            # Insights
            st.subheader("Key Insights")
            insights = analysis.get('price_insights', [])
            for i, insight in enumerate(insights, 1):
                st.write(f"{i}. {insight}")
            
            # Recommendations
            st.subheader("Recommendations")
            recommendations = analysis.get('recommendations', [])
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
            
            # Download PDF
            st.divider()
            st.subheader("Download Report")
            
            pdf_bytes = pdf_gen.generate_analysis_report(
                analysis, 
                st.session_state.analysis_platform.upper()
            )
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name=f"quick_analysis_{st.session_state.analysis_platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        else:  # Deep Analysis
            st.subheader("Executive Report")
            st.write(analysis.get('final_report', 'No report generated'))
            
            st.divider()
            st.subheader("Agent Outputs")
            
            for agent_result in analysis.get('detailed_results', []):
                with st.expander(f"🤖 {agent_result['agent']}"):
                    st.write(agent_result['output'])
            
            st.divider()
            st.metric("Tasks Completed", analysis.get('tasks_completed', 0))


elif page == "Reports":
    st.header("Analysis Reports")
    st.markdown("View and download AI-generated analysis reports")
    
    # Filter to only show AI analysis reports
    reports = list(db_manager.reports.find({
        'report_type': {'$in': ['quick_analysis', 'deep_analysis']}
    }).sort('generated_at', -1))
    
    if reports:
        st.metric("Total AI Reports", len(reports))
        
        # Display reports with download option
        for i, report in enumerate(reports[:20]):
            report_type = report.get('report_type', 'Unknown').replace('_', ' ').title()
            platform = report.get('platform', 'N/A').upper()
            date = report.get('generated_at', 'N/A')
            products_analyzed = report.get('products_analyzed', 0)
            
            with st.expander(
                f"📊 {report_type} - {platform} | {date} | {products_analyzed} products",
                expanded=(i == 0)  # Expand first report by default
            ):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write("**Report Details:**")
                    st.write(f"- **Type:** {report_type}")
                    st.write(f"- **Platform:** {platform}")
                    st.write(f"- **Products Analyzed:** {products_analyzed}")
                    st.write(f"- **Generated At:** {date}")
                
                with col2:
                    # Download button for each report
                    if report.get('analysis'):
                        try:
                            pdf_bytes = pdf_gen.generate_analysis_report(
                                report['analysis'],
                                platform
                            )
                            
                            st.download_button(
                                label="📥 Download PDF",
                                data=pdf_bytes,
                                file_name=f"{report_type.lower().replace(' ', '_')}_{platform}_{i}.pdf",
                                mime="application/pdf",
                                key=f"download_{report['_id']}",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"PDF generation failed: {str(e)}")
                
                # Show analysis summary
                st.divider()
                st.write("**Analysis Summary:**")
                
                analysis = report.get('analysis', {})
                
                if report_type == "Quick Analysis":
                    # Show key metrics
                    if 'price_range' in analysis:
                        price_range = analysis['price_range']
                        st.write(f"- **Price Range:** ₹{price_range.get('min', 0):,.0f} - ₹{price_range.get('max', 0):,.0f}")
                        st.write(f"- **Average Price:** ₹{price_range.get('average', 0):,.0f}")
                    
                    if 'price_insights' in analysis:
                        st.write("**Key Insights:**")
                        for insight in analysis['price_insights'][:3]:
                            st.write(f"  • {insight}")
                    
                    if 'recommendations' in analysis:
                        st.write("**Top Recommendations:**")
                        for rec in analysis['recommendations'][:3]:
                            st.write(f"  • {rec}")
                
                else:  # Deep Analysis
                    if 'final_report' in analysis:
                        st.write(analysis['final_report'][:500] + "...")
                    
                    if 'tasks_completed' in analysis:
                        st.write(f"- **Tasks Completed:** {analysis['tasks_completed']}")
    else:
        st.info("No AI analysis reports found. Generate reports from the AI Insights page.")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; font-size: 0.875rem;'>
        Retail Intelligence Platform | Powered by AI & Cloud Technologies
    </div>
    """,
    unsafe_allow_html=True,
)
