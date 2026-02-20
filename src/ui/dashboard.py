# src/ui/dashboard.py
import streamlit as st
from src.scrapers.amazon_scraper import AmazonScraper
from src.scrapers.flipkart_scraper import FlipkartScraper
from src.database.mongo_manager import db_manager
from src.agents.analysis_agent import ProductAnalysisAgent
from src.utils.pdf_generator import ReportPDFGenerator
import pandas as pd
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Intelligence Platform",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design system (mirrors the HTML/CSS v2 theme) ─────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 24px 28px 40px !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #13151f !important;
    border-right: 1px solid rgba(255,255,255,.05) !important;
}
[data-testid="stSidebar"] * { color: #8d94a8 !important; }
[data-testid="stSidebar"] .sidebar-brand { color: #fff !important; font-weight: 700 !important; }

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 8px 10px !important;
    border-radius: 7px !important;
    color: #8d94a8 !important;
    font-size: 13px !important;
    font-weight: 450 !important;
    transition: background .15s, color .15s !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #1c1f2e !important;
    color: #c8cdd8 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] + label,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: rgba(37,99,235,.18) !important;
    color: #fff !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] { gap: 2px !important; }
[data-testid="stSidebar"] input[type="radio"] { accent-color: #3b82f6 !important; }

/* Sidebar metrics */
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #1c1f2e !important;
    border-radius: 7px !important;
    padding: 8px 10px !important;
    margin-bottom: 6px !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] { font-size: 10px !important; letter-spacing: .5px !important; text-transform: uppercase; }
[data-testid="stSidebar"] [data-testid="stMetricValue"] { font-size: 18px !important; font-weight: 700 !important; color: #fff !important; }
[data-testid="stSidebar"] [data-testid="stMetricDelta"] { display: none !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #fff !important; font-size: 12px !important; font-weight: 600 !important; letter-spacing: .8px; text-transform: uppercase; opacity: .45; margin-bottom: 6px !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.06) !important; }

/* ── Main content ── */
.stApp { background: #f0f2f7 !important; }

/* Page title (h1 override) */
h1 {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #0d0f1a !important;
    letter-spacing: -.1px !important;
    margin-bottom: 4px !important;
}
h2 {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #0d0f1a !important;
    margin-bottom: 10px !important;
}
h3 {
    font-size: 13.5px !important;
    font-weight: 600 !important;
    color: #0d0f1a !important;
    margin-bottom: 8px !important;
}
p { color: #4b5263; font-size: 13px; }

/* ── KPI cards (metric blocks) ── */
[data-testid="stMetric"] {
    background: #fff !important;
    border: 1px solid rgba(0,0,0,.07) !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,.07) !important;
    position: relative;
    overflow: hidden;
    transition: box-shadow .15s, transform .15s !important;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,.09) !important;
    transform: translateY(-1px) !important;
}
/* Top colored strip per column handled by kpi-card classes below */
[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #8b93a5 !important;
    text-transform: uppercase !important;
    letter-spacing: .4px !important;
}
[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #0d0f1a !important;
    letter-spacing: -1px !important;
}
[data-testid="stMetricDelta"] {
    font-size: 11px !important;
    color: #8b93a5 !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border-radius: 7px !important;
    height: 36px !important;
    box-shadow: none !important;
    transition: background .15s, box-shadow .15s !important;
}
.stButton > button[kind="primary"] {
    background: #2563eb !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 1px 3px rgba(37,99,235,.35) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 4px 14px rgba(37,99,235,.4) !important;
}
.stButton > button:not([kind="primary"]) {
    background: #f8f9fc !important;
    border: 1px solid rgba(0,0,0,.12) !important;
    color: #0d0f1a !important;
}
.stButton > button:not([kind="primary"]):hover { background: #eef0f5 !important; }

/* ── Inputs / Selects ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stSlider > div {
    border-radius: 7px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    border-color: rgba(0,0,0,.12) !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.14) !important;
}
label[data-testid="stWidgetLabel"] {
    font-size: 11.5px !important;
    font-weight: 600 !important;
    color: #4b5263 !important;
    letter-spacing: .1px !important;
}

/* ── Radio (analysis type) ── */
.stRadio label {
    font-size: 13px !important;
    padding: 8px 12px !important;
    border: 1px solid rgba(0,0,0,.10) !important;
    border-radius: 7px !important;
    margin-bottom: 6px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}
.stRadio label:has(input:checked) {
    border-color: #3b82f6 !important;
    background: rgba(37,99,235,.07) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #fff !important;
    border: 1px solid rgba(0,0,0,.07) !important;
    border-radius: 11px !important;
    padding: 3px !important;
    gap: 2px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,.05) !important;
    width: fit-content !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    color: #4b5263 !important;
    padding: 6px 16px !important;
    height: auto !important;
    border: none !important;
}
.stTabs [aria-selected="true"][data-baseweb="tab"] {
    background: #f0f2f7 !important;
    color: #0d0f1a !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,.05) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,0,0,.07) !important;
    border-radius: 11px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 2px rgba(0,0,0,.05) !important;
}

/* ── Expanders ── */
details {
    background: #fff !important;
    border: 1px solid rgba(0,0,0,.07) !important;
    border-radius: 11px !important;
    margin-bottom: 7px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,.05) !important;
    overflow: hidden !important;
}
details summary {
    padding: 13px 16px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #0d0f1a !important;
}

/* ── Cards (st.container) ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    background: #fff;
    border-radius: 14px;
    border: 1px solid rgba(0,0,0,.07);
    box-shadow: 0 1px 4px rgba(0,0,0,.07);
    padding: 20px 22px;
    margin-bottom: 14px;
}

/* ── Alerts / notices ── */
.stAlert {
    border-radius: 11px !important;
    border-left-width: 3px !important;
    font-size: 13px !important;
}
.stSuccess { border-color: #059669 !important; background: rgba(5,150,105,.06) !important; color: #047857 !important; }
.stInfo    { border-color: #2563eb !important; background: rgba(37,99,235,.06) !important; color: #1d4ed8 !important; }
.stWarning { border-color: #d97706 !important; background: rgba(217,119,6,.07) !important; color: #92400e !important; }
.stError   { border-color: #e11d48 !important; background: rgba(225,29,72,.06) !important; color: #9f1239 !important; }

/* ── Download / Link buttons ── */
.stDownloadButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    border-radius: 7px !important;
    height: 34px !important;
    background: #f8f9fc !important;
    border: 1px solid rgba(0,0,0,.12) !important;
    color: #0d0f1a !important;
}
.stDownloadButton > button:hover { background: #eef0f5 !important; }

/* ── KPI top-strip colours (via custom HTML cards) ── */
.kpi-card {
    background: #fff;
    border: 1px solid rgba(0,0,0,.07);
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,.07);
    position: relative;
    overflow: hidden;
    transition: box-shadow .15s, transform .15s;
}
.kpi-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.09); transform: translateY(-2px); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.kpi-blue::before   { background: linear-gradient(90deg,#2563eb,#3b82f6); }
.kpi-green::before  { background: linear-gradient(90deg,#047857,#059669); }
.kpi-amber::before  { background: linear-gradient(90deg,#d97706,#f59e0b); }
.kpi-violet::before { background: linear-gradient(90deg,#7c3aed,#8b5cf6); }

.kpi-label { font-size: 11px; font-weight: 600; color: #8b93a5; text-transform: uppercase; letter-spacing: .4px; margin-bottom: 10px; }
.kpi-value { font-size: 30px; font-weight: 700; color: #0d0f1a; letter-spacing: -1.5px; line-height: 1; margin-bottom: 4px; }
.kpi-sub   { font-size: 11px; color: #8b93a5; }

/* Quick action tiles */
.action-tile {
    background: #f8f9fc;
    border: 1px solid rgba(0,0,0,.07);
    border-radius: 11px;
    padding: 16px;
    cursor: pointer;
    transition: border-color .15s, box-shadow .15s, background .15s;
}
.action-tile:hover { border-color: #3b82f6; box-shadow: 0 4px 16px rgba(0,0,0,.09); background: #fff; }
.action-tile-icon {
    width: 34px; height: 34px;
    border-radius: 7px;
    background: rgba(37,99,235,.1);
    color: #2563eb;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 10px;
    font-size: 16px;
}
.action-tile-name { font-size: 13px; font-weight: 600; color: #0d0f1a; margin-bottom: 4px; }
.action-tile-desc { font-size: 11px; color: #8b93a5; line-height: 1.4; }

/* Drop cards */
.drop-card {
    background: #fff;
    border: 1px solid rgba(0,0,0,.07);
    border-radius: 11px;
    padding: 13px 16px;
    box-shadow: 0 1px 2px rgba(0,0,0,.05);
    margin-bottom: 7px;
    transition: box-shadow .15s;
}
.drop-card:hover { box-shadow: 0 4px 14px rgba(0,0,0,.09); }
.drop-card-hd { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 6px; }
.drop-card-title { font-size: 13px; font-weight: 500; color: #0d0f1a; flex: 1; line-height: 1.4; }
.drop-pct { font-size: 12px; font-weight: 700; color: #059669; background: rgba(5,150,105,.1); padding: 2px 8px; border-radius: 100px; white-space: nowrap; }
.drop-card-meta { display: flex; gap: 16px; flex-wrap: wrap; font-size: 12px; color: #4b5263; }
.drop-card-meta strong { color: #0d0f1a; font-weight: 600; }

/* Badges */
.badge { display: inline-flex; align-items: center; padding: 2px 7px; border-radius: 100px; font-size: 11px; font-weight: 600; }
.b-amazon  { background: rgba(217,119,6,.1); color: #d97706; }
.b-flipkart{ background: rgba(37,99,235,.1); color: #2563eb; }
.b-green   { background: rgba(5,150,105,.1); color: #047857; }
.b-rose    { background: rgba(225,29,72,.1); color: #be123c; }
.b-muted   { background: #eef0f5; color: #8b93a5; }

/* Insight / rec list */
.insight-list, .rec-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 7px; }
.insight-item {
    display: flex; gap: 10px; padding: 10px 14px;
    background: #f8f9fc; border-radius: 7px;
    border-left: 2px solid #3b82f6; font-size: 13px; color: #0d0f1a;
}
.insight-num { color: #3b82f6; font-weight: 700; font-size: 12px; min-width: 18px; }
.rec-item {
    display: flex; gap: 8px; padding: 9px 13px;
    background: rgba(5,150,105,.05); border-radius: 7px;
    border-left: 2px solid #059669; font-size: 13px; color: #0d0f1a;
}
.rec-arrow { color: #059669; font-weight: 700; }

/* Report card */
.report-card {
    background: #fff; border: 1px solid rgba(0,0,0,.07);
    border-radius: 11px; padding: 16px 18px;
    box-shadow: 0 1px 2px rgba(0,0,0,.05);
    margin-bottom: 8px;
}

/* Divider */
hr { border-color: rgba(0,0,0,.07) !important; margin: 14px 0 !important; }

/* Scrollbar */
::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,.15); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Cached resources ──────────────────────────────────────────────────
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
agent    = get_agent()
pdf_gen  = get_pdf_gen()


# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:4px 0 16px;border-bottom:1px solid rgba(255,255,255,.06);margin-bottom:10px">
      <div style="width:32px;height:32px;border-radius:7px;background:linear-gradient(140deg,#2563eb,#7c3aed);display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;flex-shrink:0;box-shadow:0 4px 12px rgba(37,99,235,.35)">R</div>
      <div>
        <div style="font-size:13px;font-weight:700;color:#fff;letter-spacing:.2px">RetailIQ</div>
        <div style="font-size:10px;color:#8d94a8;letter-spacing:.15px">Intelligence Platform</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:9.5px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#8d94a8;opacity:.45;margin-bottom:4px">Main</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["Dashboard", "Data Collection", "Product Explorer", "Price Analytics", "AI Insights", "Reports"],
        label_visibility="collapsed",
    )

    st.divider()

    # System status
    st.markdown('<div style="font-size:9.5px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#8d94a8;opacity:.45;margin-bottom:8px">System Status</div>', unsafe_allow_html=True)

    stats = db_manager.get_database_stats()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Products", stats["total_products"])
    with col_b:
        st.metric("Platforms", len(stats["platforms"]))
    with col_c:
        st.metric("Reports", stats["total_reports"])

    st.markdown("""
    <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#8d94a8;opacity:.75;margin-top:8px">
      <div style="width:6px;height:6px;border-radius:50%;background:#059669;box-shadow:0 0 6px #059669;flex-shrink:0"></div>
      <span>API Connected</span>
    </div>
    """, unsafe_allow_html=True)


# ── Helper: KPI card HTML ─────────────────────────────────────────────
def kpi_card(label, value, sub, color="blue"):
    return f"""
    <div class="kpi-card kpi-{color}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>"""


def fmt_price(v):
    if v is None: return "—"
    return f"₹{v:,.0f}"


def trend_badge(t):
    t = (t or "stable").lower()
    if t == "down":   return '<span class="badge b-green">Drop</span>'
    if t == "up":     return '<span class="badge b-rose">Rise</span>'
    return '<span class="badge b-muted">Stable</span>'


def platform_badge(p):
    p = (p or "").upper()
    if p == "AMAZON":   return f'<span class="badge b-amazon">{p}</span>'
    if p == "FLIPKART": return f'<span class="badge b-flipkart">{p}</span>'
    return f'<span class="badge b-muted">{p}</span>'


# ══════════════════════════════════════════════════════ DASHBOARD
if page == "Dashboard":
    st.markdown("**Real-time competitive intelligence and market analysis**",
                help="Live data from MongoDB")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("Total Products", stats["total_products"],
                             "Actively tracked", "blue"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Price Drops", stats["price_drops"],
                             "Opportunities found", "green"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Price Increases", stats["price_increases"],
                             "Trending upward", "amber"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("Platforms", len(stats["platforms"]),
                             "Multi-platform", "violet"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Actions
    with st.container():
        st.markdown("### Quick Actions")
        qa1, qa2, qa3, qa4 = st.columns(4)
        with qa1:
            st.markdown("""<div class="action-tile">
              <div class="action-tile-icon">↓</div>
              <div class="action-tile-name">Collect Data</div>
              <div class="action-tile-desc">Scrape products from Amazon &amp; Flipkart</div>
            </div>""", unsafe_allow_html=True)
        with qa2:
            st.markdown("""<div class="action-tile">
              <div class="action-tile-icon">⊙</div>
              <div class="action-tile-name">Explore Products</div>
              <div class="action-tile-desc">Browse and compare across platforms</div>
            </div>""", unsafe_allow_html=True)
        with qa3:
            st.markdown("""<div class="action-tile">
              <div class="action-tile-icon">⚡</div>
              <div class="action-tile-name">AI Analysis</div>
              <div class="action-tile-desc">Generate Gemini-powered market insights</div>
            </div>""", unsafe_allow_html=True)
        with qa4:
            st.markdown("""<div class="action-tile">
              <div class="action-tile-icon">▦</div>
              <div class="action-tile-name">Price Analytics</div>
              <div class="action-tile-desc">Track price movements and trends</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent Activity
    hd1, hd2 = st.columns([6, 1])
    with hd1:
        st.markdown("### Recent Activity")
    with hd2:
        if st.button("Refresh", key="dash_refresh"):
            st.rerun()

    recent = db_manager.get_all_products(limit=15)
    if recent:
        rows = []
        for p in recent:
            rows.append({
                "Platform": (p.get("platform") or "N/A").upper(),
                "Product":  (p.get("title") or "Unknown")[:70],
                "Price":    fmt_price(p.get("current_price")),
                "Trend":    (p.get("price_trend") or "stable").capitalize(),
                "Last Updated": str(p.get("last_seen", "—"))[:16],
            })
        st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)
    else:
        st.info("No activity yet. Start by collecting data from the Data Collection page.")


# ══════════════════════════════════════════════════════ DATA COLLECTION
elif page == "Data Collection":
    st.header("Data Collection")
    st.caption("Scrape product data from e-commerce platforms and save to the database")

    with st.container():
        st.markdown("#### Collection Settings")
        search_query = st.text_input("Search Query",
                                     placeholder="e.g. wireless headphones, laptop, smartphone")

        col1, col2, col3 = st.columns(3)
        with col1:
            platform = st.selectbox("Platform", ["Amazon", "Flipkart"])
        with col2:
            category = st.selectbox("Category",
                                    ["Electronics", "Clothing", "Cosmetics",
                                     "Groceries", "Home & Kitchen"])
        with col3:
            max_results = st.number_input("Max Results", min_value=1, max_value=50, value=10)

        clicked = st.button("Start Collection", type="primary", width='stretch')

    if clicked:
        if not search_query:
            st.warning("Enter a search query to continue")
        else:
            scraper = scrapers[platform.lower()]
            with st.spinner(f"Scraping {platform} for \"{search_query}\"…"):
                pb = st.progress(0)
                pb.progress(20)
                products = scraper.search_products(search_query, max_results=max_results)
                pb.progress(70)

                if products:
                    for p in products:
                        p["category"] = category.lower()
                    results = db_manager.save_products_bulk(products)
                    pb.progress(100)
                    pb.empty()

                    st.success(f"Collection complete — {len(products)} products processed")

                    m1, m2, m3 = st.columns(3)
                    m1.metric("New Products",     results.get("inserted", 0))
                    m2.metric("Updated",          results.get("updated",  0))
                    m3.metric("Errors",           results.get("errors",   0))

                    st.markdown("#### Collected Products")
                    df_data = []
                    for p in products:
                        df_data.append({
                            "Title":    (p.get("title", "Unknown") or "")[:55],
                            "Price":    fmt_price(p.get("price")),
                            "Rating":   f"{p['rating']:.1f}" if p.get("rating") else "—",
                            "Platform": (p.get("platform") or "").upper(),
                        })
                    st.dataframe(pd.DataFrame(df_data), width='stretch', hide_index=True)
                else:
                    pb.empty()
                    st.error("No products found. Try a different search query.")


# ══════════════════════════════════════════════════════ PRODUCT EXPLORER
elif page == "Product Explorer":
    st.header("Product Explorer")
    st.caption("Search, browse and compare products across platforms")

    tab1, tab2, tab3 = st.tabs(["Multi-Platform Search", "Browse Database", "Compare Products"])

    # ── Tab 1: Multi-Platform Search
    with tab1:
        st.markdown("#### Search All Platforms Simultaneously")
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            ms_query = st.text_input("Search Query",
                                     placeholder="e.g. wireless headphones, laptop",
                                     key="ms_q")
        with col2:
            ms_max = st.number_input("Per Platform", min_value=1, max_value=10,
                                     value=5, key="ms_max")
        with col3:
            ms_cat = st.selectbox("Category",
                                  ["Electronics", "Clothing", "Cosmetics",
                                   "Groceries", "Home & Kitchen"], key="ms_cat")

        c1, c2 = st.columns(2)
        with c1: ms_amazon   = st.checkbox("Amazon",   value=True, key="ms_am")
        with c2: ms_flipkart = st.checkbox("Flipkart", value=True, key="ms_fk")

        if st.button("Search All Platforms", type="primary", width='stretch'):
            if not ms_query:
                st.warning("Enter a search query")
            elif not (ms_amazon or ms_flipkart):
                st.warning("Select at least one platform")
            else:
                results = {}
                total   = 0
                pb  = st.progress(0)
                msg = st.empty()

                if ms_amazon:
                    msg.text("Searching Amazon…")
                    pb.progress(25)
                    try:
                        prods = AmazonScraper().search_products(ms_query, ms_max)
                        if prods:
                            for p in prods: p["category"] = ms_cat.lower()
                            results["amazon"] = prods
                            total += len(prods)
                            db_manager.save_products_bulk(prods)
                    except Exception as e:
                        st.error(f"Amazon search failed: {e}")
                    pb.progress(50)

                if ms_flipkart:
                    msg.text("Searching Flipkart…")
                    pb.progress(75)
                    try:
                        prods = FlipkartScraper().search_products(ms_query, ms_max)
                        if prods:
                            for p in prods: p["category"] = ms_cat.lower()
                            results["flipkart"] = prods
                            total += len(prods)
                            db_manager.save_products_bulk(prods)
                    except Exception as e:
                        st.error(f"Flipkart search failed: {e}")
                    pb.progress(100)

                msg.empty(); pb.empty()

                if total > 0:
                    st.success(f"Found {total} products across {len(results)} platform(s)")

                    all_prices = [p["price"] for prods in results.values()
                                  for p in prods if p.get("price")]
                    if all_prices:
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Lowest Price",  fmt_price(min(all_prices)))
                        m2.metric("Highest Price", fmt_price(max(all_prices)))
                        m3.metric("Average Price", fmt_price(sum(all_prices)/len(all_prices)))

                    for pl_name, prods in results.items():
                        st.markdown(f"**{pl_name.upper()} — {len(prods)} results**")
                        rows = [{"Title": p.get("title","")[:60],
                                 "Price": fmt_price(p.get("price")),
                                 "Rating": f"{p['rating']:.1f}" if p.get("rating") else "—"}
                                for p in prods]
                        st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)
                else:
                    st.error("No products found. Try different search terms.")

    # ── Tab 2: Browse Database
    with tab2:
        st.markdown("#### Browse Collected Products")
        col1, col2, col3 = st.columns(3)
        with col1:
            br_platform = st.selectbox("Platform",
                ["All"] + [p.upper() for p in stats["platforms"]], key="br_pl")
        with col2:
            br_category = st.selectbox("Category",
                ["All"] + [c.capitalize() for c in stats.get("categories", [])], key="br_cat")
        with col3:
            br_view = st.selectbox("Filter",
                ["All Products", "Price Drops", "Trending"], key="br_view")

        if br_view == "Price Drops":
            products = db_manager.get_price_drops(min_percent=5.0)
        elif br_view == "Trending":
            products = db_manager.get_trending_products(limit=50)
        elif br_platform == "All":
            products = db_manager.get_all_products(limit=100)
        else:
            products = db_manager.get_products_by_platform(br_platform.lower())

        if br_category != "All":
            products = [p for p in products
                        if (p.get("category") or "").lower() == br_category.lower()]

        st.caption(f"{len(products)} products")

        if products:
            rows = []
            for p in products:
                rows.append({
                    "Product":  (p.get("title") or "")[:65],
                    "Platform": (p.get("platform") or "N/A").upper(),
                    "Price":    fmt_price(p.get("current_price")),
                    "Rating":   f"{p['current_rating']:.1f}" if p.get("current_rating") else "—",
                    "Trend":    (p.get("price_trend") or "stable").capitalize(),
                    "Change":   f"{p.get('price_change_percent',0):.1f}%",
                    "Scrapes":  p.get("times_scraped", 0),
                })
            st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)

            st.divider()
            st.markdown("#### Product Details")
            sel = st.selectbox("Select product",
                               range(len(products)),
                               format_func=lambda i: (products[i].get("title","")[:60] + "…"),
                               key="br_detail")
            if sel is not None:
                p = products[sel]
                d1, d2 = st.columns(2)
                with d1:
                    st.markdown("**Product Information**")
                    st.write(f"**Title:** {p.get('title')}")
                    st.write(f"**Platform:** {(p.get('platform') or '').upper()}")
                    st.write(f"**Category:** {(p.get('category') or '').capitalize()}")
                    st.write(f"**Price:** {fmt_price(p.get('current_price'))}")
                    st.write(f"**Rating:** {p.get('current_rating','—')}")
                with d2:
                    st.markdown("**Tracking Data**")
                    st.write(f"**First Seen:** {str(p.get('first_seen','—'))[:16]}")
                    st.write(f"**Last Updated:** {str(p.get('last_seen','—'))[:16]}")
                    st.write(f"**Times Scraped:** {p.get('times_scraped',0)}")
                    st.write(f"**Trend:** {(p.get('price_trend') or 'stable').capitalize()}")
                    st.write(f"**Change:** {(p.get('price_change_percent') or 0):.1f}%")

                if p.get("price_history") and len(p["price_history"]) > 1:
                    st.divider()
                    st.markdown("**Price History**")
                    h = pd.DataFrame(p["price_history"])
                    h["timestamp"] = pd.to_datetime(h["timestamp"])
                    st.line_chart(h.sort_values("timestamp").set_index("timestamp")["price"],
                                  width='stretch')
        else:
            st.info("No products found for the selected filters.")

    # ── Tab 3: Compare Products
    with tab3:
        st.markdown("#### Compare Two Products Side by Side")
        all_prods = db_manager.get_all_products(limit=200)

        if len(all_prods) > 1:
            col1, col2 = st.columns(2)
            with col1:
                p1i = st.selectbox("Product 1", range(len(all_prods)),
                                   format_func=lambda i: f"{all_prods[i].get('platform','?').upper()} — {all_prods[i].get('title','')[:50]}",
                                   key="cmp1")
            with col2:
                p2i = st.selectbox("Product 2", range(len(all_prods)),
                                   format_func=lambda i: f"{all_prods[i].get('platform','?').upper()} — {all_prods[i].get('title','')[:50]}",
                                   index=1, key="cmp2")

            if st.button("Run Comparison", type="primary", width='stretch'):
                p1, p2 = all_prods[p1i], all_prods[p2i]
                cmp = {
                    "Attribute": ["Platform", "Title", "Current Price", "Rating",
                                  "Trend", "Times Scraped", "First Seen"],
                    "Product 1": [
                        (p1.get("platform") or "?").upper(),
                        (p1.get("title") or "?")[:55],
                        fmt_price(p1.get("current_price")),
                        f"{p1['current_rating']:.1f}" if p1.get("current_rating") else "—",
                        (p1.get("price_trend") or "stable").capitalize(),
                        p1.get("times_scraped", 0),
                        str(p1.get("first_seen","—"))[:10],
                    ],
                    "Product 2": [
                        (p2.get("platform") or "?").upper(),
                        (p2.get("title") or "?")[:55],
                        fmt_price(p2.get("current_price")),
                        f"{p2['current_rating']:.1f}" if p2.get("current_rating") else "—",
                        (p2.get("price_trend") or "stable").capitalize(),
                        p2.get("times_scraped", 0),
                        str(p2.get("first_seen","—"))[:10],
                    ],
                }
                st.dataframe(pd.DataFrame(cmp), width='stretch', hide_index=True)

                pr1, pr2 = p1.get("current_price"), p2.get("current_price")
                if pr1 and pr2:
                    st.divider()
                    st.markdown("#### Price Analysis")
                    cheaper = "Product 1" if pr1 < pr2 else "Product 2"
                    diff    = abs(pr1 - pr2)
                    pct     = diff / max(pr1, pr2) * 100
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Cheaper Option",       cheaper)
                    m2.metric("Price Difference",     fmt_price(diff))
                    m3.metric("Saving",               f"{pct:.1f}%")
                    st.info(f"{cheaper} is {fmt_price(diff)} cheaper ({pct:.1f}% saving)")
        else:
            st.info("Need at least 2 products in the database. Collect more data first.")


# ══════════════════════════════════════════════════════ PRICE ANALYTICS
elif page == "Price Analytics":
    st.header("Price Analytics")
    st.caption("Track price changes and identify market opportunities")

    tab1, tab2, tab3 = st.tabs(["Price Drops", "Price Increases", "Distribution"])

    with tab1:
        st.markdown("#### Products with Price Reductions")
        min_drop    = st.slider("Minimum price drop %", 0, 50, 10)
        price_drops = db_manager.get_price_drops(min_percent=min_drop)

        if price_drops:
            st.success(f"{len(price_drops)} opportunity{'ies' if len(price_drops)!=1 else 'y'} found")
            for p in price_drops[:25]:
                savings = (p.get("highest_price") or 0) - (p.get("current_price") or 0)
                pct     = abs(p.get("price_change_percent") or 0)
                st.markdown(f"""
                <div class="drop-card">
                  <div class="drop-card-hd">
                    <div class="drop-card-title">{p.get('title','—')}</div>
                    <div class="drop-pct">{pct:.1f}% off</div>
                  </div>
                  <div class="drop-card-meta">
                    <span>{platform_badge(p.get('platform','?'))}</span>
                    <span>Now: <strong>{fmt_price(p.get('current_price'))}</strong></span>
                    <span>Was: <strong>{fmt_price(p.get('highest_price'))}</strong></span>
                    <span style="color:#059669">Save: <strong>{fmt_price(savings)}</strong></span>
                    {"<span>Rating: <strong>" + str(p.get('current_rating','—')) + "</strong></span>" if p.get('current_rating') else ""}
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info(f"No products with >{min_drop}% price drop found.")

    with tab2:
        st.markdown("#### Products with Price Increases")
        prods       = db_manager.get_all_products(limit=100)
        price_ups   = [p for p in prods if p.get("price_trend") == "up"]

        if price_ups:
            st.warning(f"{len(price_ups)} product{'s' if len(price_ups)!=1 else ''} with price increases")
            rows = []
            for p in sorted(price_ups, key=lambda x: x.get("price_change_percent",0), reverse=True)[:20]:
                rows.append({
                    "Product":  (p.get("title",""))[:60],
                    "Platform": (p.get("platform","")).upper(),
                    "Current":  fmt_price(p.get("current_price")),
                    "Previous": fmt_price(p.get("lowest_price")),
                    "Change":   f"+{(p.get('price_change_percent') or 0):.1f}%",
                })
            st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)
        else:
            st.info("No price increases detected.")

    with tab3:
        st.markdown("#### Price Distribution Overview")
        all_prods = db_manager.get_all_products(limit=100)
        prices    = [p["current_price"] for p in all_prods if p.get("current_price")]

        if prices:
            m1, m2, m3 = st.columns(3)
            avg = sum(prices) / len(prices)
            m1.metric("Average Price", fmt_price(avg))
            m2.metric("Lowest",        fmt_price(min(prices)))
            m3.metric("Highest",       fmt_price(max(prices)))
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Distribution**")
            st.bar_chart(pd.Series(prices, name="Price (₹)"), width='stretch')
        else:
            st.info("No pricing data available.")


# ══════════════════════════════════════════════════════ AI INSIGHTS
elif page == "AI Insights":
    st.header("AI Insights")
    st.caption("Generate intelligent market insights powered by Gemini AI")

    if "current_analysis" not in st.session_state:
        st.session_state.current_analysis = None

    with st.container():
        st.markdown("#### Analysis Configuration")
        col1, col2, col3 = st.columns(3)

        with col1:
            analysis_type = st.radio(
                "Analysis Type",
                ["Quick Analysis", "Deep Analysis (Multi-Agent)"],
                help="Quick: ~10 sec | Deep: 5–6 min"
            )
        with col2:
            ai_platform = st.selectbox("Platform",
                                       ["All Platforms", "Amazon", "Flipkart"])
        with col3:
            avail_cats = stats.get("categories", [])
            ai_category = st.selectbox(
                "Category",
                ["All Categories"] + [c.capitalize() for c in avail_cats]
            )
            query = {}
            if ai_platform != "All Platforms":
                query["platform"] = ai_platform.lower()
            if ai_category != "All Categories":
                query["category"] = ai_category.lower()
            count = db_manager.products.count_documents(query)
            st.metric("Products to Analyse", count)

        run_btn = st.button("Run Analysis", type="primary", width='stretch')

    if run_btn:
        products = list(db_manager.products.find(query))
        if not products:
            st.warning("No products found for the selected filters. Collect data first.")
        else:
            st.session_state.analysis_platform = ai_platform
            st.session_state.analysis_category = ai_category

            if analysis_type == "Quick Analysis":
                with st.spinner(f"Analysing {len(products)} products…"):
                    result = agent.analyze_products(products)
                if "error" not in result:
                    st.session_state.current_analysis = result
                    st.session_state.analysis_type    = "quick"
                    db_manager.save_report({
                        "report_type": "quick_analysis",
                        "platform":   ai_platform.lower() if ai_platform != "All Platforms" else "all",
                        "category":   ai_category.lower() if ai_category != "All Categories" else "all",
                        "analysis":   result,
                        "products_analyzed": len(products),
                    })
                    st.rerun()
                else:
                    st.error(f"Analysis failed: {result['error']}")
            else:
                st.info(f"Deep analysis will take 5–6 minutes for {len(products)} products.")
                from src.agents.crew_manager import crew_manager
                with st.spinner("Multi-agent analysis in progress…"):
                    result = crew_manager.analyze_products(products)
                if "error" not in result:
                    st.session_state.current_analysis = result
                    st.session_state.analysis_type    = "deep"
                    db_manager.save_report({
                        "report_type": "deep_analysis",
                        "platform":   ai_platform.lower() if ai_platform != "All Platforms" else "all",
                        "category":   ai_category.lower() if ai_category != "All Categories" else "all",
                        "analysis":   result,
                        "products_analyzed": len(products),
                    })
                    st.rerun()
                else:
                    st.error(f"Analysis failed: {result['error']}")

    # Show result
    if st.session_state.current_analysis is not None:
        st.divider()
        an    = st.session_state.current_analysis
        atype = st.session_state.get("analysis_type", "quick")
        apl   = st.session_state.get("analysis_platform", "—")
        acat  = st.session_state.get("analysis_category", "—")

        # Scope pill
        st.markdown(
            f'<div style="display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:600;'
            f'color:#2563eb;background:rgba(37,99,235,.1);padding:3px 10px;border-radius:100px;'
            f'text-transform:uppercase;letter-spacing:.2px;margin-bottom:14px">'
            f'{apl} · {acat}</div>',
            unsafe_allow_html=True
        )

        if atype == "quick":
            pr = an.get("price_range", {})
            m1, m2, m3 = st.columns(3)
            m1.metric("Products Analysed", an.get("total_products", 0))
            m2.metric("Average Price",     fmt_price(pr.get("average")))
            m3.metric("Price Range",
                      f"{fmt_price(pr.get('min'))} – {fmt_price(pr.get('max'))}")

            top = an.get("top_rated_product", {})
            if top.get("title"):
                st.markdown("**Top Rated Product**")
                top_meta = (
                    "<span style='color:#8b93a5'>"
                    + str(top.get("rating"))
                    + " stars &middot; "
                    + fmt_price(top.get("price"))
                    + "</span>"
                ) if top.get("rating") else ""
                st.markdown(
                    f'<div style="padding:12px 14px;background:rgba(124,58,237,.05);'
                    f'border:1px solid rgba(124,58,237,.15);border-radius:11px;font-size:13px">'
                    f'<strong>{top["title"]}</strong> {top_meta}</div>',
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)

            best = an.get("best_value_product", {})
            if best.get("title"):
                st.markdown("**Best Value**")
                best_reason = (
                    "<div style='color:#4b5263;font-size:12px;margin-top:4px'>"
                    + best.get("reason", "")
                    + "</div>"
                ) if best.get("reason") else ""
                st.markdown(
                    f'<div style="padding:12px 14px;background:rgba(5,150,105,.05);'
                    f'border:1px solid rgba(5,150,105,.15);border-radius:11px;font-size:13px">'
                    f'<strong>{best["title"]}</strong>{best_reason}</div>',
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)

            insights = an.get("price_insights", [])
            if insights:
                st.markdown("**Key Insights**")
                items = "".join(
                    f'<li class="insight-item"><span class="insight-num">{i}</span>{ins}</li>'
                    for i, ins in enumerate(insights, 1)
                )
                st.markdown(f'<ul class="insight-list">{items}</ul>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            recs = an.get("recommendations", [])
            if recs:
                st.markdown("**Recommendations**")
                items = "".join(
                    f'<li class="rec-item"><span class="rec-arrow">→</span>{r}</li>'
                    for r in recs
                )
                st.markdown(f'<ul class="rec-list">{items}</ul>', unsafe_allow_html=True)

            st.divider()
            pdf_bytes = pdf_gen.generate_analysis_report(an, f"{apl} - {acat}")
            st.download_button(
                "Download PDF Report", data=pdf_bytes,
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf", width='stretch'
            )

        else:  # deep
            st.markdown("**Executive Report**")
            st.markdown(
                f'<div style="padding:16px;background:#f8f9fc;border:1px solid rgba(0,0,0,.07);'
                f'border-radius:11px;font-size:13px;color:#4b5263;line-height:1.7">'
                f'{(an.get("final_report") or "No report generated").replace(chr(10),"<br/>")}'
                f'</div>',
                unsafe_allow_html=True
            )
            st.divider()
            for agent_res in an.get("detailed_results", []):
                with st.expander(agent_res.get("agent", "Agent")):
                    st.write(agent_res.get("output", ""))
            st.divider()
            st.metric("Tasks Completed", an.get("tasks_completed", 0))
            st.info("Deep analysis reports are automatically saved to the database.")


# ══════════════════════════════════════════════════════ REPORTS
elif page == "Reports":
    hd1, hd2 = st.columns([6, 1])
    with hd1:
        st.header("Reports")
    with hd2:
        if st.button("Refresh", key="rpt_refresh"):
            st.rerun()
    st.caption("View and download AI-generated analysis reports")

    reports = list(db_manager.reports.find(
        {"report_type": {"$in": ["quick_analysis", "deep_analysis"]}}
    ).sort("generated_at", -1))

    if reports:
        st.success(f"{len(reports)} report{'s' if len(reports)!=1 else ''} in database")

        for i, r in enumerate(reports[:30]):
            rtype   = (r.get("report_type") or "").replace("_", " ").title()
            rl_pf   = "All Platforms" if r.get("platform") == "all" else (r.get("platform") or "?").upper()
            rl_cat  = "All Categories" if r.get("category") == "all" else (r.get("category") or "?").capitalize()
            rd      = str(r.get("generated_at","—"))[:16]
            cnt     = r.get("products_analyzed", 0)

            with st.expander(f"{rtype}  ·  {rl_pf}  ·  {rl_cat}  ·  {cnt} products  ·  {rd}",
                             expanded=(i == 0)):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**Type:** {rtype}  |  **Platform:** {rl_pf}  |  **Category:** {rl_cat}")
                    st.caption(f"Generated: {rd}  ·  {cnt} products analysed")

                    an = r.get("analysis", {})
                    if r.get("report_type") == "quick_analysis":
                        if "price_range" in an:
                            pr = an["price_range"]
                            st.write(f"Price range: {fmt_price(pr.get('min'))} — {fmt_price(pr.get('max'))} · Avg: {fmt_price(pr.get('average'))}")
                        for ins in (an.get("price_insights") or [])[:3]:
                            st.caption(f"• {ins}")
                        for rec in (an.get("recommendations") or [])[:3]:
                            st.caption(f"→ {rec}")
                    else:
                        final = (an.get("final_report") or "")[:280]
                        if final:
                            st.caption(final + "…")

                with col2:
                    if r.get("analysis"):
                        try:
                            pdf_bytes = pdf_gen.generate_analysis_report(
                                r["analysis"], f"{rl_pf} - {rl_cat}"
                            )
                            st.download_button(
                                "Download PDF", data=pdf_bytes,
                                file_name=f"report_{rtype.lower().replace(' ','_')}_{i}.pdf",
                                mime="application/pdf",
                                key=f"dl_{r['_id']}",
                                width='stretch'
                            )
                        except Exception as e:
                            st.error(f"PDF failed: {e}")
    else:
        st.info("No reports found. Generate one from the AI Insights page.")


# ── Footer ────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    '<div style="text-align:center;color:#8b93a5;font-size:12px">'
    'Retail Intelligence Platform · Powered by Gemini AI</div>',
    unsafe_allow_html=True
)
