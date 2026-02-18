# Low-Level Design Document
## AI-Powered Retail Intelligence Platform

**Version:** 2.0  
**Date:** February 2026  
**Author:** Development Team  
**Status:** Production Ready

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
10. [Recent Updates](#10-recent-updates)

---

## 1. Introduction

### 1.1 Project Overview

The **AI-Powered Retail Intelligence Platform** is a comprehensive automated system designed to provide competitive intelligence and market analysis for retail businesses. It scrapes product data from multiple e-commerce platforms, tracks pricing trends over time, and generates AI-powered insights using both single and multi-agent systems to support strategic decision-making.

### 1.2 Business Problem

Retail businesses face critical challenges:
- **Manual price monitoring** is time-consuming, error-prone, and impossible to scale
- **Competitive intelligence** requires constant market surveillance across multiple platforms
- **Price optimization** decisions lack data-driven insights and historical context
- **Multi-platform comparison** is difficult to track and analyze manually
- **Category-specific analysis** requires domain expertise and extensive research time

### 1.3 Solution

Our platform addresses these challenges through:
- **Automated multi-platform data collection** from Amazon and Flipkart
- **Intelligent product tracking** with unique IDs and price history
- **Real-time price tracking** with historical trend analysis
- **AI-powered insights** using single agent (quick) and multi-agent systems (deep)
- **Professional web dashboard** with interactive data visualization
- **Multi-platform search** and side-by-side product comparison
- **Category-specific analysis** with flexible filtering options
- **Persistent analysis results** that survive navigation
- **Downloadable PDF reports** for all analyses

### 1.4 Key Features

#### Core Functionality
- ✅ Multi-platform web scraping (Amazon, Flipkart)
- ✅ Intelligent product tracking with composite unique IDs
- ✅ Price history tracking with trend analysis
- ✅ Automated duplicate detection and data merging
- ✅ Single AI agent for quick insights (5-10 seconds)
- ✅ Multi-agent CrewAI system for deep analysis (5-6 minutes)
- ✅ Professional web dashboard with modern UI
- ✅ PDF report generation with downloadable archives
- ✅ Cloud-based MongoDB storage

#### Advanced Features
- ✅ **Multi-platform simultaneous search** - Search Amazon and Flipkart at once
- ✅ **Product comparison tool** - Side-by-side analysis with savings calculation
- ✅ **Category filtering** - Analyze by Electronics, Clothing, Cosmetics, etc.
- ✅ **Persistent analysis** - Results survive tab switching
- ✅ **Report archiving** - All AI reports saved and downloadable
- ✅ **CI/CD pipeline** - Automated testing and deployment
- ✅ **Session state management** - Improved user experience

---

## 2. System Architecture

### 2.1 High-Level Architecture (Updated)
```
┌─────────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │         Streamlit Dashboard (Modern Professional UI)         │  │
│  │                                                              │  │
│  │  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │  │
│  │  │Dashboard │   Data   │ Product  │  Price   │    AI    │  │  │
│  │  │   Home   │Collection│ Explorer │Analytics │ Insights │  │  │
│  │  └──────────┴──────────┴──────────┴──────────┴──────────┘  │  │
│  │                                                              │  │
│  │  New Features:                                              │  │
│  │  • Multi-platform simultaneous search                       │  │
│  │  • Product comparison (side-by-side)                        │  │
│  │  • Category-based filtering                                 │  │
│  │  • Persistent analysis results                              │  │
│  │  • Report download archive                                  │  │
│  │  • Session state management                                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────────────┐
│                    APPLICATION LOGIC LAYER                          │
│  ┌──────────────┬──────────────┬──────────────────────────────────┐│
│  │   Scraping   │   Analysis   │      Data Management            ││
│  │   Engine     │   Engine     │         Engine                  ││
│  │              │              │                                  ││
│  │ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┬──────────────────┐││
│  │ │  Base    │ │ │  Single  │ │ │ Upsert   │   Query          │││
│  │ │ Scraper  │ │ │  Agent   │ │ │ Logic    │  Optimizer       │││
│  │ │          │ │ │(Gemini)  │ │ │          │                  │││
│  │ └──────────┘ │ └──────────┘ │ └──────────┴──────────────────┘││
│  │ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┬──────────────────┐││
│  │ │ Amazon   │ │ │  Multi   │ │ │  Price   │   Report         │││
│  │ │ Scraper  │ │ │  Agent   │ │ │ History  │  Generator       │││
│  │ │          │ │ │(CrewAI)  │ │ │ Tracking │  (PDF)           │││
│  │ └──────────┘ │ │5 Agents  │ │ └──────────┴──────────────────┘││
│  │ ┌──────────┐ │ └──────────┘ │ ┌──────────────────────────────┐││
│  │ │Flipkart  │ │              │ │  Session State Manager       │││
│  │ │ Scraper  │ │              │ │  (Persistent Analysis)       │││
│  │ └──────────┘ │              │ └──────────────────────────────┘││
│  └──────────────┴──────────────┴──────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
                              ↓ MongoDB Protocol (TLS)
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA PERSISTENCE LAYER                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              MongoDB Atlas (Cloud Database)                   │  │
│  │  ┌────────────────┬──────────────────┬─────────────────────┐ │  │
│  │  │   Products     │  Price History   │    Reports          │ │  │
│  │  │  Collection    │    (Embedded)    │   Collection        │ │  │
│  │  │                │                  │   (AI Analysis)     │ │  │
│  │  └────────────────┴──────────────────┴─────────────────────┘ │  │
│  │                                                              │  │
│  │  Indexes: unique_id, platform, category, price_trend        │  │
│  │  Features: Upsert logic, computed metrics, time series      │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ HTTPS/REST APIs
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES LAYER                          │
│  ┌──────────────┬──────────────┬──────────────────────────────────┐│
│  │  Amazon.in   │ Flipkart.com │  AI Services                    ││
│  │  (Web        │  (Web        │  • Google Gemini 2.5 Flash      ││
│  │   Scraping)  │   Scraping)  │  • Groq (Llama 3.3 70B)         ││
│  │              │              │  • CrewAI Multi-Agent           ││
│  └──────────────┴──────────────┴──────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Interaction Flow (Enhanced)
```
User Request
    ↓
Dashboard (UI Layer) + Session State
    ↓
[Decision Point]
    ├─→ Multi-Platform Search?
    │       ↓
    │   Parallel Scraping (Amazon + Flipkart)
    │       ↓
    │   Merge Results + Price Comparison
    │       ↓
    │   Database (Upsert Logic)
    │
    ├─→ Product Comparison?
    │       ↓
    │   Fetch Products from Database
    │       ↓
    │   Calculate Price Diff + Recommendations
    │       ↓
    │   Display Side-by-Side
    │
    ├─→ Category-Filtered Analysis?
    │       ↓
    │   Build Query (Platform + Category)
    │       ↓
    │   Fetch Filtered Products
    │       ↓
    │   AI Agent (Single or Multi)
    │       ↓
    │   Store in Session State (Persistent)
    │       ↓
    │   Save to Reports Collection
    │       ↓
    │   Generate PDF
    │
    └─→ Browse/Visualization?
            ↓
        Database Query (Filtered)
            ↓
        Display with Charts
```

### 2.3 Design Principles

1. **Modularity**: Each component is independent and replaceable
2. **Scalability**: Easy to add new platforms, categories, or AI models
3. **Maintainability**: Clear separation of concerns with defined interfaces
4. **Reliability**: Multi-layer error handling with graceful degradation
5. **Performance**: Caching, efficient queries, and optimized data structures
6. **User Experience**: Session state management for seamless navigation
7. **Extensibility**: Plugin architecture for new features

---

## 3. Module Design

### 3.1 Web Scraping Module (Enhanced)

#### 3.1.1 Base Scraper Class

**File**: `src/scrapers/base_scraper.py`

**Responsibilities**:
- Initialize Selenium WebDriver with Chrome
- Handle HTTP requests with retry logic
- Parse HTML content with BeautifulSoup
- Manage delays to avoid rate limiting
- Handle errors gracefully

**Key Methods**:
```python
class BaseScraper:
    def __init__(self):
        # Initialize scraper configuration
        # Setup user agents, delays, retry logic
        
    def setup_driver(self):
        # Configure Selenium with Chrome (headless)
        # Install ChromeDriver automatically
        
    def fetch_with_selenium(self, url: str) -> str:
        # Fetch page using Selenium
        # Handle timeouts and errors
        
    def parse_html(self, html: str) -> BeautifulSoup:
        # Parse HTML with BeautifulSoup4
        # Extract structured data
```

**Design Pattern**: Template Method Pattern

#### 3.1.2 Platform-Specific Scrapers

**Amazon Scraper** (`src/scrapers/amazon_scraper.py`)
- Extends `BaseScraper`
- Amazon-specific CSS selectors
- Extracts: ASIN (product ID), title, price, rating, reviews, image URL
- Handles Amazon's dynamic content loading

**Flipkart Scraper** (`src/scrapers/flipkart_scraper.py`)
- Extends `BaseScraper`
- Flipkart-specific HTML parsing
- Extracts: Product ID, title, price, rating, reviews
- Handles Flipkart's JavaScript rendering

**Common Interface**:
```python
def search_products(self, query: str, max_results: int) -> List[Dict]:
    """
    Search for products on the platform
    
    Returns:
        List of product dictionaries with standardized schema
    """
```

**New Feature: Multi-Platform Search**
- Dashboard can invoke multiple scrapers simultaneously
- Results are merged with platform identification
- Automatic price comparison across platforms

### 3.2 Database Module (Production-Ready)

#### 3.2.1 MongoDB Manager

**File**: `src/database/mongo_manager.py`

**Key Features**:
- **Intelligent Upsert Logic**: Insert new products or update existing ones
- **Price History Tracking**: Array-based time series storage
- **Computed Metrics**: Automatic trend calculation (up/down/stable)
- **Index Management**: Optimized queries with compound indexes
- **Category Support**: Products organized by category
- **Report Storage**: Separate collection for AI analysis reports

**Core Methods**:
```python
class MongoDBManager:
    def upsert_product(self, product_data: Dict) -> Dict:
        """
        Smart insert/update logic based on unique_id
        
        Process:
        1. Check if product exists (platform + product_id)
        2. If NEW → Insert with initial metadata
        3. If EXISTS → Update + add price history entry
        4. Calculate trends and metrics
        """
        
    def _insert_new_product(self, ...):
        """
        Create new product document with:
        - Unique ID (platform_productID)
        - Initial price history
        - Tracking metadata
        """
        
    def _update_existing_product(self, ...):
        """
        Update existing product:
        - Add to price_history array
        - Recalculate min/max/avg prices
        - Update price_trend and change_percent
        - Increment times_scraped
        """
        
    def get_price_drops(self, min_percent: float):
        """Query products with significant price reductions"""
        
    def get_products_by_category(self, category: str):
        """Get all products in a specific category"""
        
    def save_report(self, report_data: Dict):
        """Save AI analysis report with metadata"""
```

**Enhanced Schema**:
```python
{
    "unique_id": "platform_productID",  # Composite unique key
    "platform": "amazon",
    "product_id": "B08N5WRWNW",
    "title": "Product Name",
    "category": "electronics",  # NEW: Category support
    "current_price": 14999.0,
    "price_history": [
        {"timestamp": ISODate, "price": 15999.0},
        {"timestamp": ISODate, "price": 14999.0}
    ],
    "price_trend": "down",
    "price_change_percent": -6.25,
    "lowest_price": 14999.0,
    "highest_price": 15999.0,
    "average_price": 15499.0,
    "times_scraped": 2,
    "first_seen": ISODate,
    "last_seen": ISODate
}
```

### 3.3 AI Agent Module (Dual-Mode)

#### 3.3.1 Single Agent (Quick Analysis)

**File**: `src/agents/analysis_agent.py`

**Purpose**: Fast insights (5-10 seconds)

**Process**:
1. Prepare product summary (token optimization)
2. Construct structured prompt with JSON schema
3. Send to Gemini 2.5 Flash API
4. Extract and validate JSON response
5. Return analysis report

**Enhanced Features**:
- Category-aware analysis
- Platform-specific insights
- Handles "All Categories" and "All Platforms" filters

**Output Structure**:
```json
{
    "total_products": 25,
    "price_range": {"min": 299, "max": 14999, "average": 4532},
    "top_rated_product": {...},
    "best_value_product": {...},
    "price_insights": [...],
    "recommendations": [...],
    "category": "electronics",  // NEW
    "platform": "amazon"        // NEW
}
```

#### 3.3.2 Multi-Agent System (Deep Analysis)

**File**: `src/agents/crew_manager.py`

**Purpose**: Comprehensive analysis (5-6 minutes)

**Agent Roles**:

1. **Data Scout**: Identifies trends, market gaps, competitive patterns
2. **Pricing Strategist**: Analyzes pricing patterns and optimization strategies
3. **Risk Assessor**: Evaluates market risks and competitive threats
4. **Demand Forecaster**: Predicts future demand and seasonal trends
5. **Report Writer**: Synthesizes all findings into executive report

**Execution Flow**:
```
Data Scout → Pricing Strategist → Risk Assessor → Demand Forecaster → Report Writer
     ↓              ↓                 ↓                  ↓                    ↓
  Trends        Strategy           Risks             Forecast          Final Report
```

**Rate Limiting**: 60-second delay between tasks to avoid API quotas

**Enhanced Features**:
- Supports category-filtered analysis
- Multi-platform aggregate insights
- Context-aware recommendations

### 3.4 Utility Modules

#### 3.4.1 PDF Generator (Enhanced)

**File**: `src/utils/pdf_generator.py`

**Features**:
- Professional formatting with ReportLab
- Metrics tables with color coding
- Insights and recommendations sections
- Platform and category context in header
- Downloadable from both Analysis and Reports pages

**New Capabilities**:
- Multi-platform report formatting
- Category-specific layouts
- Better error handling

#### 3.4.2 Helper Functions

**File**: `src/utils/helpers.py`

**Functions**:
- `clean_price()`: Extract numeric values from various currency formats
  - Handles: ₹1,234 | 999.99 | $1234.50
  - Fixed: Decimal number detection
- `clean_rating()`: Parse rating values from text
- `random_delay()`: Anti-bot detection delays

### 3.5 UI Module (Modern & Feature-Rich)

**File**: `src/ui/dashboard.py`

**New Architecture**:
- **Session State Management**: Persistent analysis results
- **Tab-based Navigation**: 6 main sections
- **Multi-platform Search**: Simultaneous scraping
- **Product Comparison**: Side-by-side analysis
- **Category Filtering**: Flexible analysis options
- **Report Archive**: Downloadable history

**Key Features**:
1. **Dashboard Home**: Metrics, quick actions, recent activity
2. **Data Collection**: Multi-platform search with progress tracking
3. **Product Explorer**: 
   - Multi-platform search tab
   - Browse database tab
   - Compare products tab
4. **Price Analytics**: Price drops, increases, distribution
5. **AI Insights**: 
   - Category filtering
   - Platform filtering
   - Persistent results
   - PDF download
6. **Reports**: AI report archive with download buttons

---

## 4. Agent Design

### 4.1 Single Agent Architecture (Category-Aware)
```
┌─────────────────────────────────────────┐
│      ProductAnalysisAgent               │
├─────────────────────────────────────────┤
│  + __init__()                           │
│  + analyze_products(products: List)     │
│  - _prepare_product_summary()           │
│  - _extract_json()                      │
│  + compare_competitors()                │
└─────────────────────────────────────────┘
          ↓
    [Gemini 2.5 Flash]
          ↓
   {Structured JSON Analysis}
      with context:
      - Platform
      - Category
      - Product count
```

**Prompt Engineering (Enhanced)**:
- Clear role: "You are a retail market analyst specializing in [category]"
- Context injection: Platform and category information
- Structured output: JSON schema with validation
- Actionable focus: Specific, measurable recommendations

### 4.2 Multi-Agent Architecture (CrewAI - Enhanced)
```
┌──────────────────────────────────────────────────────────┐
│              RetailIntelligenceCrew                      │
│              (Category + Platform Aware)                 │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   ┌────────────┐   ┌────────────┐   ┌────────────┐    │
│   │Data Scout  │──>│  Pricing   │──>│   Risk     │    │
│   │   Agent    │   │ Strategist │   │  Assessor  │    │
│   │            │   │            │   │            │    │
│   │Context:    │   │Uses Scout  │   │Uses Scout  │    │
│   │Platform +  │   │findings +  │   │+ Pricing   │    │
│   │Category    │   │Context     │   │findings    │    │
│   └────────────┘   └────────────┘   └────────────┘    │
│         │                                    │          │
│         v                                    v          │
│   ┌────────────┐                    ┌────────────┐    │
│   │  Demand    │<───────────────────│  Report    │    │
│   │ Forecaster │                    │  Writer    │    │
│   │            │                    │            │    │
│   │Uses Scout  │                    │Synthesizes │    │
│   │findings    │                    │all agents  │    │
│   └────────────┘                    └────────────┘    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Enhanced Agent Specialization**:

| Agent | Goal | Input Context | Output |
|-------|------|---------------|--------|
| Data Scout | Find trends & gaps | Platform, Category, Products | Market opportunities |
| Pricing Strategist | Optimize pricing | Scout findings + Product prices | Price recommendations |
| Risk Assessor | Identify threats | Scout + Pricing insights | Risk mitigation plans |
| Demand Forecaster | Predict demand | Scout findings + Historical data | Demand forecasts |
| Report Writer | Synthesize findings | All agent outputs + Context | Executive report |

**Context Propagation**:
- Each agent receives platform and category context
- Later agents access earlier agents' outputs
- Final report includes comprehensive context

---

## 5. Sequence Flow

### 5.1 Multi-Platform Search Flow (New)
```
sequenceDiagram
    participant U as User
    participant D as Dashboard
    participant AS as Amazon Scraper
    participant FS as Flipkart Scraper
    participant DB as Database
    
    U->>D: Enter search query + select platforms
    D->>D: Create parallel scraping tasks
    
    par Amazon Search
        D->>AS: search_products(query, max_results)
        AS->>AS: Initialize Selenium
        AS->>E: Fetch Amazon search results
        E-->>AS: HTML content
        AS->>AS: Parse & extract products
        AS-->>D: List[AmazonProduct]
    and Flipkart Search
        D->>FS: search_products(query, max_results)
        FS->>FS: Initialize Selenium
        FS->>E2: Fetch Flipkart search results
        E2-->>FS: HTML content
        FS->>FS: Parse & extract products
        FS-->>D: List[FlipkartProduct]
    end
    
    D->>D: Merge results with platform tags
    D->>D: Calculate price comparison metrics
    D->>DB: save_products_bulk(all_products)
    
    loop For each product
        DB->>DB: upsert_product()
    end
    
    DB-->>D: {inserted: X, updated: Y}
    D->>D: Generate comparison summary
    D-->>U: Display results + price analysis
```

### 5.2 Category-Filtered AI Analysis Flow (Enhanced)
```
sequenceDiagram
    participant U as User
    participant D as Dashboard
    participant SS as Session State
    participant DB as Database
    participant A as AI Agent
    participant G as Gemini API
    
    U->>D: Select platform + category + analysis type
    D->>D: Build MongoDB query
    note over D: query = {<br/>  platform: "amazon",<br/>  category: "electronics"<br/>}
    
    D->>DB: find(query)
    DB-->>D: Filtered products
    
    alt Quick Analysis
        D->>A: analyze_products(products, context)
        A->>A: Prepare summary with context
        A->>G: Generate analysis (with category context)
        G-->>A: JSON response
        A-->>D: Analysis report
    else Deep Analysis
        D->>CrewAI: analyze_products(products, context)
        CrewAI->>CrewAI: Sequential agent execution
        CrewAI-->>D: Comprehensive report
    end
    
    D->>SS: Store analysis in session_state
    D->>DB: save_report(report_data)
    D->>PDF: generate_pdf(analysis, context)
    D-->>U: Display analysis + download button
    
    U->>D: Switch to different tab
    D->>SS: Retrieve analysis from session_state
    D-->>U: Display same analysis (persistent!)
```

### 5.3 Product Comparison Flow (New)
```
sequenceDiagram
    participant U as User
    participant D as Dashboard
    participant DB as Database
    
    U->>D: Navigate to Compare tab
    D->>DB: get_all_products(limit=200)
    DB-->>D: All products
    
    U->>D: Select Product 1 + Product 2
    U->>D: Click "Compare Products"
    
    D->>D: Extract comparison data
    D->>D: Calculate price difference
    D->>D: Calculate percentage savings
    D->>D: Determine cheaper option
    D->>D: Compare ratings
    D->>D: Generate recommendation
    
    D-->>U: Display comparison table
    D-->>U: Show price analysis
    D-->>U: Show rating comparison
    D-->>U: Display recommendation
```

---

## 6. Database Design

### 6.1 Collections Schema (Enhanced)

#### 6.1.1 Products Collection (Updated)
```javascript
{
  // Unique Identifier
  "_id": ObjectId("..."),
  "unique_id": "amazon_B08N5WRWNW",  // platform_productID
  
  // Product Information
  "platform": "amazon",
  "product_id": "B08N5WRWNW",
  "title": "Sony WH-1000XM5 Wireless Headphones",
  "category": "electronics",  // NEW: Category support
  "url": "https://amazon.in/...",
  "image_url": "https://...",
  
  // Current State
  "current_price": 25990.0,
  "current_rating": 4.6,
  "current_reviews": "1,234",
  "in_stock": true,
  "last_seen": ISODate("2026-02-16T10:30:00Z"),
  
  // Historical Tracking
  "first_seen": ISODate("2026-01-15T08:00:00Z"),
  "price_history": [
    {
      "timestamp": ISODate("2026-01-15T08:00:00Z"),
      "price": 29990.0
    },
    {
      "timestamp": ISODate("2026-02-08T10:30:00Z"),
      "price": 25990.0
    }
  ],
  "rating_history": [
    {
      "timestamp": ISODate("2026-01-15T08:00:00Z"),
      "rating": 4.5
    },
    {
      "timestamp": ISODate("2026-02-08T10:30:00Z"),
      "rating": 4.6
    }
  ],
  
  // Computed Metrics (Auto-calculated)
  "price_trend": "down",  // up/down/stable
  "price_change_percent": -13.3,
  "lowest_price": 25990.0,
  "highest_price": 29990.0,
  "average_price": 27990.0,
  "times_scraped": 2,
  
  // Metadata
  "created_at": ISODate("2026-01-15T08:00:00Z"),
  "updated_at": ISODate("2026-02-16T10:30:00Z")
}
```

#### 6.1.2 Reports Collection (Enhanced)
```javascript
{
  "_id": ObjectId("..."),
  "report_type": "quick_analysis",  // or "deep_analysis"
  "platform": "amazon",  // or "all" for all platforms
  "category": "electronics",  // NEW: Category context
  "analysis": {
    "total_products": 25,
    "price_range": {...},
    "insights": [...],
    "recommendations": [...]
  },
  "products_analyzed": 25,
  "generated_at": ISODate("2026-02-16T10:35:00Z")
}
```

### 6.2 Indexes (Optimized)
```javascript
// Unique composite index for product tracking
db.products.createIndex(
  { platform: 1, product_id: 1 },
  { unique: true, name: "unique_product" }
)

// Query optimization indexes
db.products.createIndex({ category: 1, platform: 1 })  // NEW
db.products.createIndex({ price_trend: 1 })
db.products.createIndex({ last_seen: -1 })
db.products.createIndex({ category: 1 })  // NEW

// Report indexes
db.reports.createIndex({ report_type: 1, generated_at: -1 })
db.reports.createIndex({ platform: 1, category: 1 })  // NEW
```

### 6.3 Query Patterns (Enhanced)
```javascript
// Multi-category analysis
db.products.find({
  platform: "amazon",
  category: { $in: ["electronics", "clothing"] }
})

// All platforms, specific category
db.products.find({
  category: "electronics"
})

// Platform + Category filtered
db.products.find({
  platform: "amazon",
  category: "electronics",
  price_trend: "down"
})

// AI reports with context
db.reports.find({
  report_type: "quick_analysis",
  platform: "all",
  category: "electronics"
}).sort({ generated_at: -1 })
```

---

## 7. Technology Stack

### 7.1 Core Technologies (Current Versions)

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Language** | Python | 3.11+ | Core development language |
| **Web Scraping** | Selenium | >=4.15.0 | Browser automation |
| | BeautifulSoup4 | >=4.12.0 | HTML parsing |
| | webdriver-manager | >=4.0.0 | ChromeDriver management |
| **AI/LLM** | Google Gemini | 2.5 Flash | Quick analysis |
| | CrewAI | >=0.80.0 | Multi-agent orchestration |
| | Groq | API | Alternative LLM (Llama 3.3) |
| **Database** | MongoDB Atlas | 7.0 | Cloud NoSQL database |
| | PyMongo | >=4.6.0 | MongoDB Python driver |
| **UI Framework** | Streamlit | >=1.29.0 | Web dashboard |
| **PDF Generation** | ReportLab | >=4.0.0 | PDF creation |
| **Data Processing** | Pandas | >=2.1.0 | Data manipulation |
| | NumPy | >=1.24.0 | Numerical operations |
| **Configuration** | python-dotenv | >=1.0.0 | Environment variables |
| | Pydantic | >=2.5.0 | Data validation |
| **Testing** | pytest | >=7.4.0 | Unit testing |
| | pytest-cov | >=4.1.0 | Coverage reporting |
| **Code Quality** | black | >=23.12.0 | Code formatting |
| | flake8 | >=6.1.0 | Linting |
| | pylint | >=3.0.0 | Static analysis |

### 7.2 Development Tools

- **Package Management**: pip, venv
- **Browser Driver**: ChromeDriver (auto-managed via webdriver-manager)
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions
- **Code Editor**: VS Code (recommended)

### 7.3 External Services

- **MongoDB Atlas**: Cloud database (Free tier: M0, 512MB-5GB)
- **Google AI Studio**: Gemini API access (Free tier: 20 requests/day)
- **Groq Cloud**: Alternative LLM API (14,400 requests/day free)
- **E-commerce Platforms**: Amazon.in, Flipkart.com (public data)

### 7.4 Architecture Decisions Rationale

#### Why Selenium over Requests?
- E-commerce sites use heavy JavaScript rendering
- Dynamic content loading requires browser execution
- Anti-bot protection bypassed with real browser
- Can handle CAPTCHA and redirects

#### Why MongoDB over SQL?
- Flexible schema for evolving product data
- Native array support for price_history (no joins needed)
- Horizontal scalability built-in
- JSON-native storage (perfect for AI outputs)
- Fast document retrieval
- Easy aggregation pipeline

#### Why CrewAI for Multi-Agent?
- Specialized agent roles (domain expertise)
- Built-in task orchestration
- Sequential and hierarchical workflows
- Easy integration with multiple LLMs
- Context sharing between agents
- Production-ready error handling

#### Why Streamlit over Flask/Django?
- Rapid prototyping (10x faster development)
- Python-native (no HTML/CSS/JS needed)
- Built-in data visualization
- Session state management
- Easy deployment (Streamlit Cloud)
- Hot reloading during development

#### Why Session State Management?
- Persistent analysis results across navigation
- Better user experience (no data loss)
- Reduces unnecessary API calls
- Supports complex workflows
- Native Streamlit feature (no external dependencies)

---

## 8. Error Handling Strategy

### 8.1 Scraping Layer

**Challenges**: Network failures, HTML structure changes, rate limiting, CAPTCHA

**Strategy**:
```python
try:
    html = fetch_with_selenium(url)
    if not html:
        logger.error("Failed to fetch page")
        return []
    
    products = parse_products(html)
    if not products:
        logger.warning("No products found")
        return []
        
except TimeoutException:
    logger.error("Page load timeout")
    # Retry with increased timeout
except Exception as e:
    logger.error(f"Scraping error: {e}")
    return []
```

**Specific Handling**:
- **Timeout**: Retry with exponential backoff (3 attempts)
- **Empty Results**: Log and return empty list (don't crash)
- **HTML Changes**: Graceful degradation, skip malformed products
- **Rate Limiting**: Random delays (2-3 seconds) between requests
- **CAPTCHA**: Notify user, provide manual intervention option

### 8.2 Database Layer

**Challenges**: Connection failures, duplicate keys, None values, data corruption

**Strategy**:
```python
try:
    result = db.products.insert_one(product)
except DuplicateKeyError:
    # Product exists, update instead
    result = db.products.update_one(
        {'unique_id': product['unique_id']},
        {'$set': updates}
    )
except ConnectionFailure:
    logger.error("MongoDB connection lost")
    # Retry with connection pool
except Exception as e:
    logger.error(f"Database error: {e}")
    return {"error": str(e)}
```

**Specific Handling**:
- **None Prices**: Filter before min/max calculations
```python
  all_prices = [p for p in prices if p is not None]
  if all_prices:
      min_price = min(all_prices)
```
- **Connection Loss**: Auto-retry with connection pooling (3 attempts)
- **Validation**: Pydantic models validate data before insertion
- **Data Corruption**: Rollback mechanism for critical operations

### 8.3 AI Agent Layer

**Challenges**: API rate limits, malformed responses, quota exhaustion, network errors

**Strategy**:
```python
try:
    response = client.models.generate_content(
        model='models/gemini-2.5-flash',
        contents=prompt
    )
    analysis = extract_json(response.text)
    
except ClientError as e:
    if '429' in str(e):  # Rate limit
        logger.warning("Rate limit hit, waiting...")
        time.sleep(60)
        return {"error": "Rate limit exceeded. Try again later."}
    elif '403' in str(e):  # Quota exceeded
        return {"error": "API quota exceeded. Check billing."}
    else:
        return {"error": f"AI API error: {str(e)}"}
        
except json.JSONDecodeError:
    logger.warning("Invalid JSON response")
    # Return raw text as fallback
    return {"raw_analysis": response.text}
```

**Specific Handling**:
- **Rate Limits**: 
  - Single agent: Show error to user
  - CrewAI: 60-second delays between tasks
- **JSON Parsing**: Fallback to raw text if JSON extraction fails
- **Quota Exceeded**: Clear user message with resolution steps
- **Timeout**: 30-second timeout for API calls, then fail gracefully

### 8.4 UI Layer (Dashboard)

**Challenges**: User input validation, session state corruption, display errors

**Strategy**:
```python
if not search_query:
    st.warning("Please enter a search query")
    return

if not (search_amazon or search_flipkart):
    st.warning("Please select at least one platform")
    return

try:
    products = scraper.search_products(search_query, max_results)
    if products:
        st.success(f"Found {len(products)} products")
    else:
        st.error("No products found. Try different keywords.")
except Exception as e:
    st.error(f"Search failed: {str(e)}")
    logger.error(f"UI error: {e}")
```

**Specific Handling**:
- **Input Validation**: Check before processing
- **Progress Indicators**: Spinners for long operations
- **Error Messages**: Clear, actionable feedback to users
- **Session State**: Initialize with defaults, validate before use

### 8.5 Logging Strategy
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Usage
logger.info("✅ Product scraped successfully")
logger.warning("⚠️ Price not found, using default")
logger.error("❌ Database connection failed")
logger.debug("🔍 Detailed debug info")
```

**Log Levels**:
- **DEBUG**: Detailed troubleshooting info (development only)
- **INFO**: Normal operations, confirmations
- **WARNING**: Recoverable issues, degraded functionality
- **ERROR**: Failures requiring attention

**Log Destinations**:
- **Console**: Development (stdout)
- **File**: Production (rotating logs)
- **Cloud**: Future (CloudWatch, Datadog)

---

## 9. Future Improvements

### 9.1 Short-term (Next 2-4 weeks)

#### 1. Additional Platform Support
- **Meesho** scraper implementation
- **Myntra** for fashion category
- **Nykaa** for cosmetics
- Unified scraper interface

#### 2. Enhanced Price Tracking
- **Price drop alerts** via email/SMS
- **Threshold-based notifications** (user-configurable)
- **Price prediction** using historical data (LSTM)
- **Price alert dashboard**

#### 3. Advanced Categorization
- **Auto-category detection** using NLP
- **Sub-category support** (e.g., Electronics > Headphones > Wireless)
- **Category-specific insights** (tailored recommendations)
- **Multi-category comparison**

### 9.2 Medium-term (1-3 months)

#### 4. Scheduled Automation
- **Cron jobs** for daily scraping (configurable schedule)
- **Background task queue** (Celery + Redis)
- **Automated report generation** (weekly/monthly)
- **Health monitoring** and auto-recovery

#### 5. Advanced Analytics
- **Competitor benchmarking** (market share analysis)
- **Demand forecasting** with ML models
- **Seasonal trend detection** (festive discounts)
- **Price elasticity analysis**

#### 6. User Management
- **Multi-user support** with authentication
- **Role-based access** (Admin, Analyst, Viewer)
- **Personal dashboards** and saved searches
- **Collaboration features** (shared reports)

### 9.3 Long-term (3-6 months)

#### 7. Machine Learning Integration
- **Price prediction models** (LSTM, Prophet)
- **Product recommendation engine**
- **Anomaly detection** for pricing errors
- **Image similarity** for product matching across platforms

#### 8. API Development
- **RESTful API** for programmatic access
- **Webhook support** for real-time updates
- **API documentation** (Swagger/OpenAPI)
- **Rate limiting** and authentication

#### 9. Scalability Improvements
- **Distributed scraping** (multiple workers)
- **Redis caching** for frequent queries
- **Database sharding** for large datasets
- **Load balancing** for high traffic
- **CDN integration** for static assets

#### 10. Enhanced Reporting
- **Custom report templates**
- **Scheduled email reports**
- **Interactive charts** (Plotly, D3.js)
- **Export to Excel** with formulas and charts
- **PowerPoint exports**

### 9.4 Technical Debt & Maintenance

- **Unit test coverage** to 80%+ (pytest)
- **Integration tests** for end-to-end flows
- **CI/CD pipeline** enhancements (GitHub Actions)
- **Code quality tools** (pylint, black, mypy)
- **Documentation auto-generation** (Sphinx)
- **Performance profiling** and optimization

### 9.5 Infrastructure

- **Containerization** (Docker, Docker Compose)
- **Orchestration** (Kubernetes for scaling)
- **Monitoring** (Prometheus, Grafana)
- **Logging aggregation** (ELK stack)
- **Backup automation** (MongoDB Atlas backups + custom)
- **Disaster recovery** plan and testing

---

## 10. Recent Updates (Version 2.0)

### 10.1 Major Features Added

#### Multi-Platform Search (February 2026)
- Simultaneous scraping from Amazon and Flipkart
- Automatic price comparison across platforms
- Merged results with platform identification
- Progress tracking for parallel operations

#### Product Comparison Tool (February 2026)
- Side-by-side product comparison
- Automatic price difference calculation
- Percentage savings computation
- Rating comparison with recommendations
- "Cheaper option" identification

#### Category-Based Analysis (February 2026)
- Filter AI analysis by category
- "All Categories" option for comprehensive analysis
- "All Platforms" option for cross-platform insights
- Context-aware AI prompts with category information
- Category metadata in reports

#### Persistent Analysis Results (February 2026)
- Session state management for analysis
- Results survive tab switching
- "Start New Analysis" button for clarity
- Reduced unnecessary API calls
- Improved user experience

#### Enhanced Reports Section (February 2026)
- Filter to show only AI analysis reports
- Download button for each report
- Platform AND category context display
- Expandable report summaries
- Better visual hierarchy

### 10.2 Technical Improvements

#### Code Quality (February 2026)
- Replaced `use_container_width` with `width` parameter
- Fixed deprecation warnings
- Black code formatting applied
- Flake8 linting passed
- Test coverage improved

#### Error Handling (February 2026)
- Better handling of None values in price calculations
- Improved clean_price() function for decimal numbers
- Enhanced database upsert logic
- Graceful degradation for failed API calls

#### CI/CD Pipeline (February 2026)
- GitHub Actions workflow configured
- Automated testing on push/PR
- Code quality checks (Black, Flake8, Pylint)
- Security scanning (Bandit)
- Dependency conflict resolution

### 10.3 Documentation Updates

#### Architecture Documentation (February 2026)
- Complete system architecture diagrams
- Enhanced sequence flows
- Multi-platform search flows
- Category-filtered analysis flows
- Product comparison workflows

#### User Experience (February 2026)
- Cleaner dashboard navigation
- Better visual feedback
- Progress indicators for long operations
- Clear success/error messages
- Context-aware help text

---

## Appendix A: Code Structure
```
retail-ai-intelligence/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                  # GitHub Actions CI/CD
├── config/
│   ├── __init__.py
│   └── settings.py                    # Pydantic settings management
├── data/                              # Local data storage
├── docs/
│   ├── LLD.md                         # This document
│   ├── ARCHITECTURE.md                # System architecture
│   └── PRESENTATION.md                # Presentation guide
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── analysis_agent.py          # Single AI agent (Gemini)
│   │   └── crew_manager.py            # Multi-agent system (CrewAI)
│   ├── database/
│   │   ├── __init__.py
│   │   └── mongo_manager.py           # MongoDB operations
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py            # Abstract base class
│   │   ├── amazon_scraper.py          # Amazon implementation
│   │   └── flipkart_scraper.py        # Flipkart implementation
│   ├── ui/
│   │   ├── __init__.py
│   │   └── dashboard.py               # Streamlit interface (enhanced)
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py                 # Utility functions
│       └── pdf_generator.py           # PDF creation
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # pytest configuration
│   ├── test_database.py               # Database tests
│   ├── test_helpers.py                # Utility tests
│   └── test_crew_ai.py                # Multi-agent tests
├── .env                               # Environment variables (not in git)
├── .gitignore                         # Git ignore rules
├── Dockerfile                         # Docker container definition
├── pytest.ini                         # pytest configuration
├── README.md                          # Project overview
├── requirements.txt                   # Python dependencies
├── requirements-lock.txt              # Locked versions
└── run_dashboard.py                   # Application launcher
```

---

## Appendix B: Key Algorithms

### B.1 Product Upsert Algorithm (Enhanced)
```python
def upsert_product(product_data):
    # 1. Generate composite unique_id
    unique_id = f"{platform}_{product_id}"
    
    # 2. Check if product exists
    existing = db.find_one({
        'platform': platform,
        'product_id': product_id
    })
    
    if existing:
        # 3a. UPDATE path
        updates = {
            'last_seen': now,
            'times_scraped': existing['times_scraped'] + 1
        }
        
        # Check if price changed
        if new_price != old_price:
            # Add to price_history
            db.update_one(
                {'_id': existing['_id']},
                {'$push': {'price_history': price_entry}}
            )
            
            # Recalculate metrics
            all_prices = get_all_prices(existing) + [new_price]
            updates.update({
                'lowest_price': min(all_prices),
                'highest_price': max(all_prices),
                'average_price': mean(all_prices),
                'price_trend': calculate_trend(old_price, new_price),
                'price_change_percent': calculate_change(old_price, new_price)
            })
        
        return update_existing(existing['_id'], updates)
    else:
        # 3b. INSERT path
        new_product = {
            'unique_id': unique_id,
            'platform': platform,
            'product_id': product_id,
            'category': category,  # NEW
            'price_history': [{'timestamp': now, 'price': price}],
            'times_scraped': 1,
            # ... other fields
        }
        return insert_new(new_product)
```

### B.2 Multi-Platform Search Algorithm (New)
```python
def multi_platform_search(query, platforms, max_results):
    results = {}
    
    # Create scraper tasks
    tasks = []
    if 'amazon' in platforms:
        tasks.append(('amazon', AmazonScraper()))
    if 'flipkart' in platforms:
        tasks.append(('flipkart', FlipkartScraper()))
    
    # Execute searches (could be parallelized)
    for platform_name, scraper in tasks:
        try:
            products = scraper.search_products(query, max_results)
            results[platform_name] = products
        except Exception as e:
            logger.error(f"{platform_name} search failed: {e}")
            results[platform_name] = []
    
    # Calculate comparison metrics
    all_prices = []
    for platform_products in results.values():
        all_prices.extend([p['price'] for p in platform_products if p.get('price')])
    
    comparison = {
        'total_found': sum(len(p) for p in results.values()),
        'lowest_price': min(all_prices) if all_prices else None,
        'highest_price': max(all_prices) if all_prices else None,
        'average_price': mean(all_prices) if all_prices else None,
        'results_by_platform': results
    }
    
    return comparison
```

### B.3 Category-Filtered Analysis Algorithm (New)
```python
def analyze_with_filters(platform, category, analysis_type):
    # Build query
    query = {}
    if platform != "All Platforms":
        query['platform'] = platform.lower()
    if category != "All Categories":
        query['category'] = category.lower()
    
    # Fetch filtered products
    products = db.products.find(query)
    
    # Add context to AI prompt
    context = {
        'platform': platform,
        'category': category,
        'product_count': len(products)
    }
    
    if analysis_type == "Quick":
        # Single agent with context
        prompt = f"""
        Analyze these {len(products)} {category} products 
        from {platform}. Focus on category-specific insights.
        [products data...]
        """
        return agent.analyze(prompt)
    else:
        # Multi-agent with context
        # Each agent receives category context
        return crew.analyze(products, context)
```

---

## Appendix C: Performance Metrics

### Current Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Scrape 10 products (single platform) | 30-45s | Includes page load, parsing |
| Multi-platform search (10 per platform) | 60-90s | Parallel execution possible |
| Quick AI Analysis | 5-10s | Single Gemini API call |
| Deep AI Analysis | 5-6 min | 5 agents, 60s delay each |
| Database Query (indexed) | <100ms | With proper indexes |
| Database Upsert (single product) | 10-20ms | Including metric calculation |
| PDF Generation | 1-2s | Including formatting |
| Dashboard Load (initial) | 2-3s | First page render |
| Dashboard Navigation | <500ms | Between tabs with session state |

### Optimization Opportunities

- **Parallel Scraping**: Run Amazon and Flipkart scrapers concurrently → 30-45s total
- **Caching**: Redis for frequent database queries → <10ms response
- **Batch Processing**: Process multiple products together → 30% faster
- **API Optimization**: Reduce CrewAI delays to 30s (if rate limits allow) → 2.5 min total
- **Index Tuning**: Additional compound indexes → <50ms queries
- **Connection Pooling**: Reuse database connections → 20% faster

---

**Document Version:** 2.0  
**Last Updated:** February 16, 2026  
**Status:** Production Ready  
**Completion:** ~85%