# Low-Level Design Document
## AI-Powered Retail Intelligence Platform

**Version:** 1.0  
**Date:** February 2026  
**Author:** [Your Name]

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Architecture](#2-system-architecture)
3. [Module Design](#3-module-design)
4. [Agent Design](#4-agent-design)
5. [Sequence Flow](#5-sequence-flow)
6. [Database Design](#6-database-design)
7. [Technology Stack](#7-technology-stack)
8. [Error Handling Strategy](#8-error-handling-strategy)
9. [Future Improvements](#9-future-improvements)

---

## 1. Introduction

### 1.1 Project Overview

The **AI-Powered Retail Intelligence Platform** is an automated system designed to provide competitive intelligence and market analysis for retail businesses. It scrapes product data from multiple e-commerce platforms, tracks pricing trends, and generates AI-powered insights to support strategic decision-making.

### 1.2 Business Problem

Retail businesses face several challenges:
- **Manual price monitoring** is time-consuming and error-prone
- **Competitive intelligence** requires constant market surveillance
- **Price optimization** decisions lack data-driven insights
- **Multi-platform comparison** is difficult to track manually

### 1.3 Solution

Our platform addresses these challenges by:
- **Automated data collection** from Amazon and Flipkart
- **Real-time price tracking** with historical analysis
- **AI-powered insights** using single and multi-agent systems
- **Professional dashboard** for data visualization and reporting

### 1.4 Key Features

- ✅ Multi-platform web scraping (Amazon, Flipkart)
- ✅ Intelligent product tracking with unique IDs
- ✅ Price history and trend analysis
- ✅ Single AI agent for quick insights
- ✅ Multi-agent CrewAI system for deep analysis
- ✅ Professional web dashboard
- ✅ PDF report generation
- ✅ Cloud-based MongoDB storage

---

## 2. System Architecture

### 2.1 High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │         Streamlit Dashboard (Professional UI)             │  │
│  │  - Data Collection  - Product Explorer  - Analytics       │  │
│  │  - AI Insights     - Reports            - Visualization   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Scrapers   │  │  AI Agents   │  │  Report Generator    │   │
│  │  - Amazon    │  │  - Gemini    │  │  - PDF Creation      │   │
│  │  - Flipkart  │  │  - CrewAI    │  │  - Data Export       │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Database Manager (MongoDB)                  │   │
│  │  - Product Storage    - Price History                    │   │
│  │  - Report Archive     - Analytics Metrics                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Amazon     │  │  Flipkart    │  │  MongoDB Atlas       │   │
│  │   India      │  │   India      │  │  (Cloud Storage)     │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Interaction Flow
```
User Request
    ↓
Dashboard (UI Layer)
    ↓
[Decision Point]
    ├─→ Data Collection? → Scraper Module → Database
    ├─→ Analysis? → AI Agent Module → Database
    └─→ Visualization? → Database → Dashboard
```

### 2.3 Design Principles

1. **Modularity**: Each component (scraper, agent, database) is independent
2. **Scalability**: Easy to add new platforms or AI models
3. **Maintainability**: Clear separation of concerns
4. **Reliability**: Error handling at every layer
5. **Performance**: Caching and efficient database queries

---

## 3. Module Design

### 3.1 Web Scraping Module

#### 3.1.1 Base Scraper Class

**File**: `src/scrapers/base_scraper.py`

**Responsibilities**:
- Initialize Selenium WebDriver
- Handle HTTP requests
- Parse HTML content
- Manage delays to avoid rate limiting

**Key Methods**:
```python
class BaseScraper:
    def __init__(self):
        # Initialize scraper configuration
        
    def setup_driver(self):
        # Configure Selenium with Chrome
        
    def fetch_with_selenium(self, url: str) -> str:
        # Fetch page using Selenium
        
    def parse_html(self, html: str) -> BeautifulSoup:
        # Parse HTML with BeautifulSoup
```

**Design Pattern**: Template Method Pattern

#### 3.1.2 Platform-Specific Scrapers

**Amazon Scraper** (`src/scrapers/amazon_scraper.py`)
- Extends `BaseScraper`
- Amazon-specific selectors and parsing logic
- Extracts: ASIN, title, price, rating, reviews

**Flipkart Scraper** (`src/scrapers/flipkart_scraper.py`)
- Extends `BaseScraper`
- Flipkart-specific selectors
- Extracts: Product ID, title, price, rating

**Common Interface**:
```python
def search_products(self, query: str, max_results: int) -> List[Dict]
```

### 3.2 Database Module

#### 3.2.1 MongoDB Manager

**File**: `src/database/mongo_manager.py`

**Key Features**:
- **Upsert Logic**: Insert new products or update existing
- **Price History Tracking**: Array-based time series storage
- **Computed Metrics**: Automatic trend calculation
- **Index Management**: Optimized queries

**Core Methods**:
```python
class MongoDBManager:
    def upsert_product(self, product_data: Dict) -> Dict:
        # Smart insert/update logic
        
    def _insert_new_product(self, ...):
        # Create new product with tracking metadata
        
    def _update_existing_product(self, ...):
        # Update product and price history
        
    def get_price_drops(self, min_percent: float):
        # Query products with price reductions
```

**Database Schema**:
```python
{
    "unique_id": "platform_productID",  # Composite key
    "platform": "amazon",
    "product_id": "B08N5WRWNW",
    "title": "Product Name",
    "current_price": 14999.0,
    "price_history": [
        {"timestamp": ISODate, "price": 15999.0},
        {"timestamp": ISODate, "price": 14999.0}
    ],
    "price_trend": "down",
    "price_change_percent": -6.25,
    "times_scraped": 5
}
```

### 3.3 AI Agent Module

#### 3.3.1 Single Agent (Quick Analysis)

**File**: `src/agents/analysis_agent.py`

**Purpose**: Fast insights (5-10 seconds)

**Process**:
1. Prepare product summary
2. Send to Gemini 2.5 Flash
3. Extract structured JSON response
4. Return analysis report

**Output Structure**:
```json
{
    "total_products": 25,
    "price_range": {"min": 299, "max": 14999, "average": 4532},
    "top_rated_product": {...},
    "best_value_product": {...},
    "price_insights": [...],
    "recommendations": [...]
}
```

#### 3.3.2 Multi-Agent System (Deep Analysis)

**File**: `src/agents/crew_manager.py`

**Purpose**: Comprehensive analysis (5-6 minutes)

**Agent Roles**:

1. **Data Scout**: Identifies trends and market gaps
2. **Pricing Strategist**: Analyzes pricing patterns
3. **Risk Assessor**: Evaluates market risks
4. **Demand Forecaster**: Predicts future demand
5. **Report Writer**: Synthesizes all findings

**Execution Flow**:
```
Data Scout → Pricing Strategist → Risk Assessor
                ↓                      ↓
         Demand Forecaster ← Report Writer
```

**Rate Limiting**: 60-second delay between tasks

### 3.4 Utility Modules

#### 3.4.1 PDF Generator

**File**: `src/utils/pdf_generator.py`

**Features**:
- Professional formatting
- Metrics tables
- Insights sections
- Downloadable reports

#### 3.4.2 Helper Functions

**File**: `src/utils/helpers.py`

- `clean_price()`: Extract numeric values from currency strings
- `clean_rating()`: Parse rating values
- `random_delay()`: Anti-bot detection

---

## 4. Agent Design

### 4.1 Single Agent Architecture
```
┌─────────────────────────────────────────┐
│      ProductAnalysisAgent               │
├─────────────────────────────────────────┤
│  + __init__()                           │
│  + analyze_products(products: List)     │
│  - _prepare_product_summary()           │
│  - _extract_json()                      │
└─────────────────────────────────────────┘
          ↓
    [Gemini 2.5 Flash]
          ↓
   {Structured JSON Analysis}
```

**Prompt Engineering**:
- Clear role definition: "You are a retail market analyst"
- Structured output format (JSON schema)
- Specific instructions for insights
- Focus on actionable recommendations

### 4.2 Multi-Agent Architecture (CrewAI)
```
┌───────────────────────────────────────────────────────┐
│              RetailIntelligenceCrew                   │
├───────────────────────────────────────────────────────┤
│                                                       │
│   ┌────────────┐   ┌────────────┐   ┌────────────┐    │
│   │Data Scout  │──>│  Pricing   │──>│   Risk     │    │
│   │   Agent    │   │ Strategist │   │  Assessor  │    │
│   └────────────┘   └────────────┘   └────────────┘    │
│         │                                    │        │
│         v                                    v        │
│   ┌────────────┐                    ┌────────────┐    │
│   │  Demand    │<───────────────────│  Report    │    │
│   │ Forecaster │                    │  Writer    │    │
│   └────────────┘                    └────────────┘    │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Agent Specialization**:

| Agent | Goal | Output |
|-------|------|--------|
| Data Scout | Find trends & gaps | Market opportunities |
| Pricing Strategist | Optimize pricing | Price recommendations |
| Risk Assessor | Identify threats | Risk mitigation plans |
| Demand Forecaster | Predict demand | Demand forecasts |
| Report Writer | Synthesize findings | Executive report |

**Task Dependencies**:
- Pricing Strategist uses Scout's findings
- Risk Assessor uses Scout + Pricing insights
- Report Writer synthesizes all outputs

---

## 5. Sequence Flow

### 5.1 Data Collection Flow
```
sequenceDiagram
    participant U as User
    participant D as Dashboard
    participant S as Scraper
    participant DB as Database
    
    U->>D: Enter search query
    D->>S: search_products(query, platform)
    S->>S: Initialize Selenium
    S->>E: Fetch search results page
    E-->>S: HTML content
    S->>S: Parse HTML & extract products
    S-->>D: List[Product]
    D->>DB: save_products_bulk(products)
    DB->>DB: For each product: upsert_product()
    DB->>DB: Check if exists (by unique_id)
    alt Product exists
        DB->>DB: Update + add price history
    else New product
        DB->>DB: Insert with metadata
    end
    DB-->>D: {inserted: X, updated: Y}
    D-->>U: Display results & stats
```

### 5.2 AI Analysis Flow
```
sequenceDiagram
    participant U as User
    participant D as Dashboard
    participant A as AI Agent
    participant DB as Database
    participant G as Gemini API
    
    U->>D: Request analysis
    D->>DB: get_products_by_platform(platform)
    DB-->>D: List[Product]
    D->>A: analyze_products(products)
    A->>A: Prepare product summary
    A->>G: Generate analysis (with prompt)
    G-->>A: JSON response
    A->>A: Extract & validate JSON
    A-->>D: Analysis report
    D->>DB: save_report(report_data)
    D->>U: Display insights
    D->>U: Offer PDF download
```

### 5.3 Price Tracking Flow
```
┌─────────────────────────────────────────────────────────┐
│  Day 1: First Scrape                                    │
│                                                         │
│  Scraper finds: Sony Headphones - ₹15,999               │
│       ↓                                                 │
│  Database: INSERT                                       │
│    {                                                    │
│      unique_id: "amazon_B08N5W...",                     │
│      current_price: 15999,                              │
│      price_history: [{price: 15999, timestamp: T1}],    │
│      times_scraped: 1                                   │
│    }                                                    │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│  Day 3: Second Scrape                                   │
│                                                         │
│  Scraper finds: Sony Headphones - ₹14,999               │
│       ↓                                                 │
│  Database: UPDATE (detected by unique_id)               │
│    {                                                    │
│      current_price: 14999,                              │
│      price_history: [                                   │
│        {price: 15999, timestamp: T1},                   │
│        {price: 14999, timestamp: T3}                    │
│      ],                                                 │
│      price_trend: "down",                               │
│      price_change_percent: -6.25,                       │
│      times_scraped: 2                                   │
│    }                                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Database Design

### 6.1 Collections Schema

#### 6.1.1 Products Collection
```javascript
{
  // Unique Identifier
  "_id": ObjectId("..."),
  "unique_id": "amazon_B08N5WRWNW",  // platform_productID
  
  // Product Information
  "platform": "amazon",
  "product_id": "B08N5WRWNW",
  "title": "Sony WH-1000XM5 Wireless Headphones",
  "category": "electronics",
  "url": "https://amazon.in/...",
  "image_url": "https://...",
  
  // Current State
  "current_price": 25990.0,
  "current_rating": 4.6,
  "current_reviews": "1,234",
  "in_stock": true,
  "last_seen": ISODate("2024-02-15T10:30:00Z"),
  
  // Historical Tracking
  "first_seen": ISODate("2024-01-15T08:00:00Z"),
  "price_history": [
    {
      "timestamp": ISODate("2024-01-15T08:00:00Z"),
      "price": 29990.0
    },
    {
      "timestamp": ISODate("2024-02-08T10:30:00Z"),
      "price": 25990.0
    }
  ],
  "rating_history": [
    {
      "timestamp": ISODate("2024-01-15T08:00:00Z"),
      "rating": 4.5
    },
    {
      "timestamp": ISODate("2024-02-08T10:30:00Z"),
      "rating": 4.6
    }
  ],
  
  // Computed Metrics
  "price_trend": "down",  // up/down/stable
  "price_change_percent": -13.3,
  "lowest_price": 25990.0,
  "highest_price": 29990.0,
  "average_price": 27990.0,
  "times_scraped": 2,
  
  // Metadata
  "created_at": ISODate("2024-01-15T08:00:00Z"),
  "updated_at": ISODate("2024-02-15T10:30:00Z")
}
```

#### 6.1.2 Reports Collection
```javascript
{
  "_id": ObjectId("..."),
  "report_type": "quick_analysis",  // or "deep_analysis"
  "platform": "amazon",
  "analysis": {
    "total_products": 25,
    "price_range": {...},
    "insights": [...],
    "recommendations": [...]
  },
  "products_analyzed": 25,
  "generated_at": ISODate("2024-02-15T10:35:00Z")
}
```

### 6.2 Indexes
```javascript
// Unique composite index for product tracking
db.products.createIndex(
  { platform: 1, product_id: 1 },
  { unique: true, name: "unique_product" }
)

// Query optimization indexes
db.products.createIndex({ category: 1, platform: 1 })
db.products.createIndex({ price_trend: 1 })
db.products.createIndex({ last_seen: -1 })
```

### 6.3 Data Flow
```
Scraper Output (Raw)
    ↓
Database Manager (Normalization)
    ↓
[Check unique_id exists?]
    ├─→ NO: Create new product document
    └─→ YES: Update existing + add to price_history
    ↓
Computed Metrics Calculation
    - price_trend (up/down/stable)
    - price_change_percent
    - min/max/average prices
    ↓
Store in MongoDB Atlas
```

---

## 7. Technology Stack

### 7.1 Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Language** | Python | 3.11+ | Core development language |
| **Web Scraping** | Selenium | 4.15.2 | Browser automation |
| | BeautifulSoup4 | 4.12.2 | HTML parsing |
| **AI/LLM** | Google Gemini | 2.5 Flash | Single agent analysis |
| | CrewAI | 0.86.0 | Multi-agent orchestration |
| | Groq | API | Alternative LLM (Llama 3.3) |
| **Database** | MongoDB Atlas | 7.0 | Cloud NoSQL database |
| | PyMongo | 4.6.1 | MongoDB Python driver |
| **UI Framework** | Streamlit | 1.29.0 | Web dashboard |
| **PDF Generation** | ReportLab | 4.0.7 | PDF creation |
| **Data Processing** | Pandas | 2.1.3 | Data manipulation |
| | NumPy | 1.24.3 | Numerical operations |

### 7.2 Development Tools

- **Package Management**: pip, venv
- **Browser Driver**: ChromeDriver (via webdriver-manager)
- **Configuration**: python-dotenv, pydantic-settings
- **Version Control**: Git

### 7.3 External Services

- **MongoDB Atlas**: Cloud database (Free tier: M0)
- **Google AI Studio**: Gemini API access
- **Groq Cloud**: Alternative LLM API
- **E-commerce Platforms**: Amazon.in, Flipkart.com

### 7.4 Architecture Decisions

#### Why Selenium over Requests?
- E-commerce sites use JavaScript rendering
- Dynamic content loading
- Anti-bot protection requires browser simulation

#### Why MongoDB over SQL?
- Flexible schema for evolving product data
- Native array support for price_history
- Horizontal scalability
- JSON-native storage

#### Why CrewAI?
- Specialized agent roles
- Built-in task orchestration
- Sequential and hierarchical workflows
- Easy integration with multiple LLMs

#### Why Streamlit?
- Rapid prototyping
- Python-native (no separate frontend needed)
- Built-in data visualization
- Easy deployment

---

## 8. Error Handling Strategy

### 8.1 Scraping Layer

**Challenge**: Network failures, HTML structure changes, rate limiting

**Strategy**:
```python
try:
    html = fetch_with_selenium(url)
    if not html:
        logger.error("Failed to fetch page")
        return []
except Exception as e:
    logger.error(f"Scraping error: {e}")
    return []
```

**Specific Handling**:
- **Timeout**: Retry with exponential backoff
- **Empty Results**: Log and return empty list (don't crash)
- **HTML Changes**: Graceful degradation, skip malformed products
- **Rate Limiting**: Random delays (2-3 seconds) between requests

### 8.2 Database Layer

**Challenge**: Connection failures, duplicate keys, None values

**Strategy**:
```python
try:
    result = db.products.insert_one(product)
except DuplicateKeyError:
    # Product exists, update instead
    result = db.products.update_one(...)
except Exception as e:
    logger.error(f"Database error: {e}")
    return {"error": str(e)}
```

**Specific Handling**:
- **None Prices**: Filter before min/max calculations
- **Connection Loss**: Retry with connection pooling
- **Validation**: Pydantic models for data validation

### 8.3 AI Agent Layer

**Challenge**: API rate limits, malformed responses, quota exhaustion

**Strategy**:
```python
try:
    response = client.models.generate_content(...)
    analysis = extract_json(response.text)
except ClientError as e:
    if '429' in str(e):  # Rate limit
        return {"error": "Rate limit exceeded. Try again later."}
    return {"error": str(e)}
```

**Specific Handling**:
- **Rate Limits**: 60-second delays between CrewAI tasks
- **JSON Parsing**: Fallback to raw text if JSON extraction fails
- **Quota Exceeded**: Clear error message to user
- **Timeout**: 30-second timeout for API calls

### 8.4 UI Layer

**Challenge**: User input validation, display errors gracefully

**Strategy**:
```python
if not search_query:
    st.warning("Please enter a search query")
    return

if products:
    st.success(f"Found {len(products)} products")
else:
    st.error("No products found. Try different keywords.")
```

**User Experience**:
- **Progress Indicators**: Spinners for long operations
- **Error Messages**: Clear, actionable feedback
- **Validation**: Input sanitization before processing

### 8.5 Logging Strategy
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Usage
logger.info("✅ Product scraped successfully")
logger.warning("⚠️ Price not found, skipping")
logger.error("❌ Database connection failed")
```

**Log Levels**:
- **INFO**: Normal operations
- **WARNING**: Recoverable issues
- **ERROR**: Failures that need attention
- **DEBUG**: Detailed troubleshooting info

---

## 9. Future Improvements

### 9.1 Short-term (Next 2-4 weeks)

#### 1. Additional Platform Support
- **Meesho** scraper implementation
- **Myntra** for fashion category
- **Nykaa** for cosmetics

#### 2. Enhanced Price Tracking
- **Price drop alerts** via email
- **Threshold-based notifications**
- **Price prediction** using historical data

#### 3. Better Categorization
- **Auto-category detection** using NLP
- **Sub-category support** (e.g., Electronics > Headphones)
- **Category-specific insights**

### 9.2 Medium-term (1-3 months)

#### 4. Scheduled Automation
- **Cron jobs** for daily scraping
- **Background task queue** (Celery)
- **Automated report generation**

#### 5. Advanced Analytics
- **Competitor benchmarking**
- **Market share analysis**
- **Seasonal trend detection**
- **Demand forecasting** using ML

#### 6. User Management
- **Multi-user support**
- **Role-based access** (Admin, Analyst, Viewer)
- **Personal dashboards**
- **Saved searches & alerts**

### 9.3 Long-term (3-6 months)

#### 7. Machine Learning Integration
- **Price prediction models** (LSTM, Prophet)
- **Product recommendation engine**
- **Anomaly detection** for pricing errors
- **Image similarity** for product matching

#### 8. API Development
- **RESTful API** for programmatic access
- **Webhook support** for real-time updates
- **API documentation** (Swagger/OpenAPI)

#### 9. Scalability Improvements
- **Distributed scraping** (multiple workers)
- **Redis caching** for frequent queries
- **Database sharding** for large datasets
- **Load balancing** for high traffic

#### 10. Enhanced Reporting
- **Custom report templates**
- **Scheduled email reports**
- **Interactive charts** (Plotly, D3.js)
- **Export to Excel** with formulas

### 9.4 Technical Debt & Maintenance

- **Unit test coverage** (pytest)
- **Integration tests** for end-to-end flows
- **CI/CD pipeline** (GitHub Actions)
- **Code quality tools** (pylint, black, mypy)
- **Documentation auto-generation** (Sphinx)

### 9.5 Infrastructure

- **Containerization** (Docker)
- **Orchestration** (Kubernetes for scaling)
- **Monitoring** (Prometheus, Grafana)
- **Logging aggregation** (ELK stack)
- **Backup automation** (MongoDB Atlas backups)

---

## 10. Deployment Architecture

### 10.1 Current Local Setup
```
Developer Machine
    ├── Python 3.11 + Virtual Environment
    ├── Streamlit Dashboard (localhost:8501)
    ├── MongoDB Atlas Connection (Cloud)
    └── Gemini/Groq API Calls (Cloud)
```

### 10.2 Proposed Production Setup
```
┌──────────────────────────────────────────────────┐
│           Streamlit Cloud (Free Tier)            │
│  - Dashboard hosting                             │
│  - Automatic HTTPS                               │
│  - Public URL                                    │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│         MongoDB Atlas (M0 Free Tier)             │
│  - Products collection                           │
│  - Reports collection                            │
│  - Automated backups                             │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│              External APIs                       │
│  - Google Gemini (AI Analysis)                   │
│  - Groq (Alternative LLM)                        │
└──────────────────────────────────────────────────┘
```

---

## Appendix A: Code Structure
```
retail-ai-intelligence/
├── src/
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py        # Abstract base class
│   │   ├── amazon_scraper.py      # Amazon implementation
│   │   └── flipkart_scraper.py    # Flipkart implementation
│   ├── database/
│   │   ├── __init__.py
│   │   └── mongo_manager.py       # Database operations
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── analysis_agent.py      # Single AI agent
│   │   └── crew_manager.py        # Multi-agent system
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py             # Utility functions
│   │   └── pdf_generator.py       # PDF creation
│   └── ui/
│       └── dashboard.py           # Streamlit interface
├── config/
│   ├── __init__.py
│   └── settings.py                # Configuration management
├── data/                          # Local data storage
├── docs/                          # Documentation
├── tests/                         # Test files
├── .env                           # Environment variables
├── requirements.txt               # Python dependencies
├── README.md                      # Project overview
└── run_dashboard.py               # Application launcher
```

---

## Appendix B: Key Algorithms

### B.1 Product Upsert Algorithm
```python
def upsert_product(product_data):
    # 1. Generate unique_id
    unique_id = f"{platform}_{product_id}"
    
    # 2. Check if product exists
    existing = db.find_one({
        'platform': platform,
        'product_id': product_id
    })
    
    if existing:
        # 3a. UPDATE path
        # - Update current fields
        # - Add to price_history if price changed
        # - Recalculate metrics (min, max, avg, trend)
        # - Increment times_scraped
        return update_existing(existing, product_data)
    else:
        # 3b. INSERT path
        # - Create new document with all fields
        # - Initialize price_history with first entry
        # - Set initial metrics
        return insert_new(product_data, unique_id)
```

### B.2 Price Trend Calculation
```python
def calculate_price_trend(old_price, new_price):
    if new_price < old_price:
        trend = "down"
        change_percent = ((new_price - old_price) / old_price) * 100
    elif new_price > old_price:
        trend = "up"
        change_percent = ((new_price - old_price) / old_price) * 100
    else:
        trend = "stable"
        change_percent = 0.0
    
    return {
        'price_trend': trend,
        'price_change_percent': change_percent
    }
```

---

## Appendix C: Performance Metrics

### Current Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Scrape 10 products | ~30-45s | Includes page load, parsing |
| Quick AI Analysis | 5-10s | Single Gemini API call |
| Deep AI Analysis | 5-6 min | 5 agents, 60s delay each |
| Database Query | <100ms | With proper indexes |
| PDF Generation | 1-2s | Including formatting |
| Dashboard Load | 2-3s | Initial page render |

### Optimization Opportunities

- **Parallel Scraping**: Run multiple scrapers concurrently
- **Caching**: Redis for frequently accessed data
- **Batch Processing**: Process multiple products together
- **API Optimization**: Reduce CrewAI delays to 30s (if rate limits allow)

---

**Document Version**: 1.0  
**Last Updated**: February 15, 2026  
**Status**: Ready for Review