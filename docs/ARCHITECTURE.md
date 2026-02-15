# System Architecture Document
## AI-Powered Retail Intelligence Platform

**Version:** 1.0  
**Date:** February 2026  
**Status:** Production Ready

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture Diagrams](#2-architecture-diagrams)
3. [Component Architecture](#3-component-architecture)
4. [Data Flow Architecture](#4-data-flow-architecture)
5. [Technology Architecture](#5-technology-architecture)
6. [Deployment Architecture](#6-deployment-architecture)
7. [Security Architecture](#7-security-architecture)
8. [Scalability Considerations](#8-scalability-considerations)

---

## 1. System Overview

### 1.1 Purpose

The Retail Intelligence Platform automates competitive intelligence gathering, price monitoring, and market analysis for e-commerce retailers.

### 1.2 Key Capabilities

- **Automated Data Collection**: Scrapes product data from Amazon and Flipkart
- **Intelligent Tracking**: Unique product identification with price history
- **AI-Powered Analysis**: Single and multi-agent insights generation
- **Professional Dashboard**: Real-time visualization and reporting
- **Cloud Storage**: Scalable MongoDB Atlas integration

### 1.3 System Boundaries

**In Scope:**
- Web scraping from public e-commerce platforms
- Product price and rating tracking
- AI-based market analysis
- Report generation and visualization

**Out of Scope:**
- User authentication/authorization (single user system)
- Payment processing
- Direct e-commerce transactions
- Real-time bidding systems

---

## 2. Architecture Diagrams

### 2.1 High-Level System Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION TIER                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Streamlit Web Dashboard                      │  │
│  │  ┌────────────┬────────────┬────────────┬──────────────┐ │  │
│  │  │ Dashboard  │  Data      │  Product   │ Price        │ │  │
│  │  │   Home     │ Collection │  Explorer  │ Analytics    │ │  │
│  │  └────────────┴────────────┴────────────┴──────────────┘ │  │
│  │  ┌────────────┬────────────────────────────────────────┐ │  │
│  │  │ AI         │         Reports                        │ │  │
│  │  │ Insights   │         Archive                        │ │  │
│  │  └────────────┴────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC TIER                        │
│  ┌──────────────┬──────────────┬──────────────────────────────┐│
│  │   Scraping   │   Analysis   │      Data Management        ││
│  │   Engine     │   Engine     │         Engine              ││
│  │              │              │                              ││
│  │ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┬──────────────┐││
│  │ │  Base    │ │ │  Single  │ │ │ Upsert   │   Query      │││
│  │ │ Scraper  │ │ │  Agent   │ │ │ Logic    │  Optimizer   │││
│  │ └──────────┘ │ └──────────┘ │ └──────────┴──────────────┘││
│  │ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┬──────────────┐││
│  │ │ Amazon   │ │ │  Multi   │ │ │  Price   │   Report     │││
│  │ │ Scraper  │ │ │  Agent   │ │ │ History  │  Generator   │││
│  │ └──────────┘ │ │ (CrewAI) │ │ └──────────┴──────────────┘││
│  │ ┌──────────┐ │ └──────────┘ │                             ││
│  │ │Flipkart  │ │              │                             ││
│  │ │ Scraper  │ │              │                             ││
│  │ └──────────┘ │              │                             ││
│  └──────────────┴──────────────┴──────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              ↓ MongoDB Protocol
┌─────────────────────────────────────────────────────────────────┐
│                        DATA TIER                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              MongoDB Atlas (Cloud)                        │  │
│  │  ┌────────────────┬──────────────────┬─────────────────┐ │  │
│  │  │   Products     │  Price History   │    Reports      │ │  │
│  │  │  Collection    │    (Embedded)    │   Collection    │ │  │
│  │  └────────────────┴──────────────────┴─────────────────┘ │  │
│  │  Indexes: unique_id, platform, category, price_trend     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTPS/API
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
│  ┌──────────────┬──────────────┬──────────────────────────────┐│
│  │  Amazon.in   │ Flipkart.com │  Google Gemini / Groq API   ││
│  │  (Scraping)  │  (Scraping)  │    (AI Analysis)            ││
│  └──────────────┴──────────────┴──────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Interaction Diagram
```
┌─────────┐         ┌──────────┐         ┌──────────┐
│  User   │────────>│Dashboard │────────>│ Scraper  │
└─────────┘         └──────────┘         └──────────┘
                         │                     │
                         │                     ↓
                         │              ┌──────────┐
                         │              │E-Commerce│
                         │              │  Sites   │
                         │              └──────────┘
                         ↓                     │
                    ┌──────────┐              │
                    │ Database │<─────────────┘
                    │ Manager  │
                    └──────────┘
                         │
                         ↓
                    ┌──────────┐
                    │   AI     │
                    │ Agents   │
                    └──────────┘
                         │
                         ↓
                    ┌──────────┐
                    │  Report  │
                    │Generator │
                    └──────────┘
                         │
                         ↓
                    ┌──────────┐
                    │   User   │
                    └──────────┘
```

### 2.3 Deployment Architecture
```
┌────────────────────────────────────────────────────────────┐
│                    Developer Machine                       │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Python 3.11 + Virtual Environment                   │ │
│  │  ┌────────────────────────────────────────────────┐  │ │
│  │  │  Streamlit Server (localhost:8501)             │  │ │
│  │  │  ├── Dashboard UI                              │  │ │
│  │  │  ├── Scraping Engine                           │  │ │
│  │  │  ├── AI Agents                                 │  │ │
│  │  │  └── Database Client                           │  │ │
│  │  └────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
                         │
                         ↓ HTTPS (MongoDB Protocol)
┌────────────────────────────────────────────────────────────┐
│                  MongoDB Atlas (Cloud)                     │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  M0 Free Tier Cluster                                │ │
│  │  - Auto-scaling: 512 MB - 5 GB                       │ │
│  │  - Automatic backups                                 │ │
│  │  - Multi-region replication                          │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
                         │
                         ↓ HTTPS (REST API)
┌────────────────────────────────────────────────────────────┐
│                    External APIs                           │
│  ┌────────────────┬────────────────────────────────────┐  │
│  │  Gemini API    │          Groq API                  │  │
│  │  (Google AI)   │      (Llama Models)                │  │
│  └────────────────┴────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## 3. Component Architecture

### 3.1 Scraping Engine

#### Architecture Pattern: **Template Method + Strategy**
```
┌──────────────────────────────────────────────────────┐
│              BaseScraper (Abstract)                  │
├──────────────────────────────────────────────────────┤
│  + setup_driver()                                    │
│  + fetch_with_selenium(url)                          │
│  + fetch_with_requests(url)                          │
│  + parse_html(html)                                  │
│  # search_products(query, max_results) [Abstract]   │
│  # _extract_product_info(element) [Abstract]        │
└──────────────────────────────────────────────────────┘
                    △
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────────────┐       ┌───────────────┐
│ AmazonScraper │       │FlipkartScraper│
├───────────────┤       ├───────────────┤
│ - base_url    │       │ - base_url    │
│ - platform    │       │ - platform    │
├───────────────┤       ├───────────────┤
│ + search_     │       │ + search_     │
│   products()  │       │   products()  │
│ - _extract_   │       │ - _extract_   │
│   product_    │       │   product_    │
│   info()      │       │   info()      │
└───────────────┘       └───────────────┘
```

**Key Responsibilities:**
- **Browser Automation**: Selenium WebDriver management
- **HTML Parsing**: BeautifulSoup4 integration
- **Data Extraction**: Platform-specific selectors
- **Rate Limiting**: Anti-bot detection avoidance

**Design Decisions:**
- Template Method: Common scraping workflow in base class
- Strategy Pattern: Platform-specific extraction strategies
- Single Responsibility: Each scraper handles one platform

### 3.2 Database Architecture

#### Architecture Pattern: **Repository + Active Record**
```
┌──────────────────────────────────────────────────────┐
│            MongoDBManager                            │
├──────────────────────────────────────────────────────┤
│  - client: MongoClient                               │
│  - db: Database                                      │
│  - products: Collection                              │
│  - reports: Collection                               │
├──────────────────────────────────────────────────────┤
│  + upsert_product(product_data) → Dict              │
│  - _insert_new_product(...) → str                   │
│  - _update_existing_product(...) → str              │
│  + get_products_by_platform(platform) → List        │
│  + get_price_drops(min_percent) → List              │
│  + get_database_stats() → Dict                      │
│  + save_report(report_data) → str                   │
└──────────────────────────────────────────────────────┘
```

**Data Model:**
```javascript
// Products Collection
{
  unique_id: "platform_productID",  // Composite key
  platform: String,
  product_id: String,
  title: String,
  current_price: Number,
  price_history: [                   // Embedded time series
    {timestamp: ISODate, price: Number}
  ],
  price_trend: String,               // Computed field
  times_scraped: Number              // Audit field
}

// Reports Collection
{
  report_type: String,
  platform: String,
  analysis: Object,                  // Flexible schema
  generated_at: ISODate
}
```

**Design Decisions:**
- **Embedded Arrays**: Price history stored with product (no joins)
- **Computed Fields**: Trends calculated on write (read optimization)
- **Flexible Schema**: Reports use Object type for AI output variety
- **Indexes**: Composite unique index prevents duplicates

### 3.3 AI Agent Architecture

#### 3.3.1 Single Agent Architecture
```
┌──────────────────────────────────────────────────────┐
│        ProductAnalysisAgent                          │
├──────────────────────────────────────────────────────┤
│  - client: GeminiClient                              │
│  - model: "gemini-2.5-flash"                         │
├──────────────────────────────────────────────────────┤
│  + analyze_products(products) → Dict                 │
│  - _prepare_product_summary(products) → str          │
│  - _extract_json(text) → Dict                        │
│  + compare_competitors(platform_data) → Dict         │
└──────────────────────────────────────────────────────┘
```

**Workflow:**
1. Receive List[Product]
2. Prepare concise summary (token optimization)
3. Construct structured prompt with JSON schema
4. Call Gemini API
5. Extract and validate JSON response
6. Return analysis report

#### 3.3.2 Multi-Agent Architecture (CrewAI)
```
┌──────────────────────────────────────────────────────┐
│         RetailIntelligenceCrew                       │
├──────────────────────────────────────────────────────┤
│  - task_delay_seconds: int                           │
├──────────────────────────────────────────────────────┤
│  + create_agents() → Dict[str, Agent]                │
│  + create_tasks(agents, data) → List[Task]           │
│  + analyze_products(products) → Dict                 │
│  - _prepare_product_summary(products) → str          │
└──────────────────────────────────────────────────────┘
                    │
                    ↓ creates
        ┌───────────────────────┐
        │   5 Specialized Agents │
        └───────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
  ┌──────────┐           ┌──────────┐
  │   Data   │           │ Pricing  │
  │  Scout   │──────────>│Strategist│
  └──────────┘           └──────────┘
        │                       │
        ↓                       ↓
  ┌──────────┐           ┌──────────┐
  │  Demand  │           │   Risk   │
  │Forecaster│           │ Assessor │
  └──────────┘           └──────────┘
        │                       │
        └───────────┬───────────┘
                    ↓
              ┌──────────┐
              │  Report  │
              │  Writer  │
              └──────────┘
```

**Design Decisions:**
- **Sequential Processing**: Agents run one after another (not parallel)
- **Context Sharing**: Later agents receive earlier agents' outputs
- **Rate Limiting**: 60-second delays between tasks
- **LLM**: Groq (Llama 3.3 70B) for cost efficiency

---

## 4. Data Flow Architecture

### 4.1 Product Collection Flow
```
┌─────────┐
│  USER   │
│ INPUT   │
└────┬────┘
     │ 1. Enter search query + select platform
     ↓
┌──────────────┐
│  Dashboard   │
│  (UI Layer)  │
└──────┬───────┘
       │ 2. Call scraper.search_products()
       ↓
┌──────────────┐
│   Scraper    │
│  (Business)  │
└──────┬───────┘
       │ 3. Selenium fetches HTML
       ↓
┌──────────────┐
│  E-Commerce  │
│   Website    │
└──────┬───────┘
       │ 4. Returns HTML
       ↓
┌──────────────┐
│   Scraper    │
│  Parse Data  │
└──────┬───────┘
       │ 5. List[Product] extracted
       ↓
┌──────────────┐
│   Database   │
│   Manager    │
└──────┬───────┘
       │ 6. For each product:
       │    - Generate unique_id
       │    - Check if exists
       │    - INSERT or UPDATE
       ↓
┌──────────────┐
│   MongoDB    │
│   Atlas      │
└──────┬───────┘
       │ 7. Return stats {inserted, updated}
       ↓
┌──────────────┐
│  Dashboard   │
│  Display     │
└──────────────┘
```

### 4.2 Price Tracking Flow
```
Time: T0 (First Scrape)
┌──────────────────────────────────┐
│ Scraper finds:                   │
│ Sony Headphones - ₹15,999        │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│ Database: unique_id NOT FOUND    │
│ Action: INSERT                   │
│ {                                │
│   unique_id: "amazon_B08..."     │
│   current_price: 15999           │
│   price_history: [               │
│     {timestamp: T0, price:15999} │
│   ]                              │
│   times_scraped: 1               │
│ }                                │
└──────────────────────────────────┘

Time: T1 (Second Scrape)
┌──────────────────────────────────┐
│ Scraper finds:                   │
│ Sony Headphones - ₹14,999        │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│ Database: unique_id FOUND        │
│ Action: UPDATE                   │
│ {                                │
│   current_price: 14999           │
│   price_history: [               │
│     {timestamp: T0, price:15999},│
│     {timestamp: T1, price:14999} │
│   ]                              │
│   price_trend: "down"            │
│   price_change_percent: -6.25    │
│   times_scraped: 2               │
│ }                                │
└──────────────────────────────────┘
```

### 4.3 AI Analysis Flow
```
┌─────────┐
│  USER   │
│ REQUEST │
└────┬────┘
     │ 1. Click "Generate Analysis"
     ↓
┌──────────────┐
│  Dashboard   │
└──────┬───────┘
       │ 2. db.get_products_by_platform()
       ↓
┌──────────────┐
│  MongoDB     │
└──────┬───────┘
       │ 3. Returns List[Product]
       ↓
┌──────────────┐
│  AI Agent    │
└──────┬───────┘
       │ 4. Prepare summary (token optimization)
       │    "Product 1: Title | ₹X | 4.5⭐"
       │    "Product 2: Title | ₹Y | 4.2⭐"
       ↓
┌──────────────┐
│ Construct    │
│ Prompt +     │
│ JSON Schema  │
└──────┬───────┘
       │ 5. API Call
       ↓
┌──────────────┐
│  Gemini API  │
└──────┬───────┘
       │ 6. JSON Response
       ↓
┌──────────────┐
│  AI Agent    │
│ Validate &   │
│ Parse JSON   │
└──────┬───────┘
       │ 7. Return {analysis}
       ↓
┌──────────────┐
│  Dashboard   │
│  Display +   │
│  Save Report │
└──────────────┘
```

---

## 5. Technology Architecture

### 5.1 Technology Stack Layers
```
┌───────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                       │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Streamlit 1.29.0                                   │ │
│  │  - Python-based web framework                       │ │
│  │  - Real-time updates via WebSocket                  │ │
│  │  - Built-in data visualization                      │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                    BUSINESS LAYER                         │
│  ┌──────────────┬──────────────┬──────────────────────┐  │
│  │  Selenium    │  CrewAI      │  ReportLab          │  │
│  │  4.15.2      │  0.86.0      │  4.0.7              │  │
│  │              │              │                      │  │
│  │ Web Driver   │ Multi-Agent  │ PDF Generation      │  │
│  │ Automation   │ Orchestration│                      │  │
│  └──────────────┴──────────────┴──────────────────────┘  │
│  ┌──────────────┬──────────────┬──────────────────────┐  │
│  │ Pandas       │ BeautifulSoup│  Pydantic           │  │
│  │ 2.1.3        │ 4.12.2       │  2.5.2              │  │
│  │              │              │                      │  │
│  │ Data Manip.  │ HTML Parsing │ Data Validation     │  │
│  └──────────────┴──────────────┴──────────────────────┘  │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                     DATA LAYER                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  PyMongo 4.6.1                                      │ │
│  │  - MongoDB Python Driver                            │ │
│  │  - Connection pooling                               │ │
│  │  - BSON serialization                               │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                        │
│  ┌──────────────┬──────────────┬──────────────────────┐  │
│  │ MongoDB Atlas│ Gemini API   │  Groq API           │  │
│  │ M0 Free Tier │ 2.5 Flash    │  Llama 3.3 70B      │  │
│  └──────────────┴──────────────┴──────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

### 5.2 Communication Protocols

| Layer | Protocol | Port | Purpose |
|-------|----------|------|---------|
| UI → Business | In-Process | N/A | Python function calls |
| Business → MongoDB | MongoDB Protocol | 27017 | Database operations |
| Business → Gemini | HTTPS REST | 443 | AI API calls |
| Business → E-commerce | HTTPS | 443 | Web scraping |
| User → Dashboard | HTTP/WebSocket | 8501 | Browser access |

---

## 6. Deployment Architecture

### 6.1 Current Deployment (Local)
```
┌────────────────────────────────────────┐
│       Developer Laptop                 │
│  OS: Windows 11                        │
│  Python: 3.11                          │
│  ┌──────────────────────────────────┐ │
│  │  Virtual Environment (venv)      │ │
│  │  ┌────────────────────────────┐  │ │
│  │  │  Streamlit Application     │  │ │
│  │  │  Port: 8501                │  │ │
│  │  └────────────────────────────┘  │ │
│  └──────────────────────────────────┘ │
└────────────────────────────────────────┘
         │ HTTPS (27017)
         ↓
┌────────────────────────────────────────┐
│     MongoDB Atlas (Cloud)              │
│     Region: US-East                    │
│     Tier: M0 (512MB - 5GB)             │
└────────────────────────────────────────┘
```

### 6.2 Proposed Production Deployment
```
┌────────────────────────────────────────────────────┐
│           Streamlit Cloud (Free Tier)              │
│  ┌──────────────────────────────────────────────┐ │
│  │  Container Instance                          │ │
│  │  - Python 3.11 runtime                       │ │
│  │  - Auto-scaling (1-2 instances)              │ │
│  │  - HTTPS enabled                             │ │
│  │  - Public URL: app.streamlit.io/...          │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
         │
         ↓ MongoDB Protocol (encrypted)
┌────────────────────────────────────────────────────┐
│           MongoDB Atlas                            │
│  ┌──────────────────────────────────────────────┐ │
│  │  M0 Cluster                                  │ │
│  │  - Multi-region replication                  │ │
│  │  - Automated backups                         │ │
│  │  - IP Whitelist: 0.0.0.0/0                   │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

### 6.3 Scaling Strategy

**Vertical Scaling (Single Instance):**
- Current: Handles 1-10 concurrent users
- Bottleneck: Selenium (single browser instance)
- Solution: Increase RAM, use headless Chrome

**Horizontal Scaling (Multiple Instances):**
- Approach: Deploy multiple Streamlit instances
- Load Balancer: Streamlit Cloud automatic
- Session Affinity: Required (Streamlit stateful)

**Database Scaling:**
- Current: M0 Free Tier (512MB)
- Next: M10 Shared ($9/month) - 2GB RAM
- Future: M20 Dedicated - Auto-sharding

---

## 7. Security Architecture

### 7.1 Security Layers
```
┌─────────────────────────────────────────┐
│     APPLICATION SECURITY                │
│  ┌───────────────────────────────────┐ │
│  │  1. Environment Variables (.env)  │ │
│  │     - API keys not in code        │ │
│  │     - .gitignore protection       │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │  2. Input Validation              │ │
│  │     - Pydantic models             │ │
│  │     - SQL injection prevention    │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│     TRANSPORT SECURITY                  │
│  ┌───────────────────────────────────┐ │
│  │  1. HTTPS/TLS Encryption          │ │
│  │     - All API calls encrypted     │ │
│  │     - MongoDB TLS 1.2+            │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│     DATA SECURITY                       │
│  ┌───────────────────────────────────┐ │
│  │  1. MongoDB Security              │ │
│  │     - Authentication required     │ │
│  │     - Role-based access           │ │
│  │     - IP whitelist                │ │
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │  2. Automated Backups             │ │
│  │     - Daily snapshots             │ │
│  │     - 7-day retention             │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### 7.2 Secrets Management

**Current Approach:**
```python
# .env file (NOT committed to Git)
GEMINI_API_KEY=xxxxx
MONGODB_URI=mongodb+srv://user:pass@cluster...
GROQ_API_KEY=xxxxx

# Loading in code
from dotenv import load_dotenv
load_dotenv()
```

**Best Practices:**
- ✅ API keys in environment variables
- ✅ .gitignore includes .env
- ✅ Separate .env for dev/prod
- ❌ No key rotation (manual)
- ❌ No secrets encryption at rest

### 7.3 Scraping Ethics & Compliance

**Rate Limiting:**
- 2-3 second delays between requests
- Respect robots.txt (if present)
- User-Agent identification

**Legal Compliance:**
- Public data only
- No authentication bypass
- No ToS violation attempts

---

## 8. Scalability Considerations

### 8.1 Current Limitations

| Component | Limitation | Impact |
|-----------|-----------|--------|
| Selenium | Single browser instance | 1 scrape at a time |
| Gemini API | 20 req/day free tier | Limited analyses |
| MongoDB | M0 (512MB) | ~10k products max |
| Streamlit | Single instance | 1-10 concurrent users |

### 8.2 Scaling Roadmap

#### Phase 1: Optimize Current Stack (0-1k products)
- ✅ Efficient database indexes
- ✅ Query optimization
- ✅ Caching frequent queries
- **No infrastructure changes needed**

#### Phase 2: Service Scaling (1k-10k products)
- Add Redis for caching
- Upgrade MongoDB to M10
- Parallel scraping (multiple Selenium instances)
- Batch processing for AI analysis

#### Phase 3: Distributed Architecture (10k-100k products)
- Containerize with Docker
- Deploy to Kubernetes
- Distributed task queue (Celery + Redis)
- Horizontal scaling of scrapers
- CDN for dashboard assets

#### Phase 4: Enterprise Scale (100k+ products)
- Microservices architecture
- Event-driven with message queues
- Real-time streaming (Kafka)
- Geo-distributed databases
- ML model deployment

### 8.3 Performance Optimization Strategies

**Database:**
- Compound indexes on (platform, category)
- Projection (return only needed fields)
- Aggregation pipeline for analytics
- Read replicas for analytics queries

**Scraping:**
- Parallel execution (asyncio)
- Proxy rotation (avoid blocks)
- Intelligent scheduling (scrape when idle)
- Incremental updates (only changed products)

**AI Agents:**
- Batch analysis (process multiple products)
- Response caching
- Model selection (fast vs. accurate)
- Token optimization (compress prompts)

---

## 9. Monitoring & Observability

### 9.1 Current Monitoring

**Logging:**
```python
import logging
logger.info("✅ Product scraped")
logger.error("❌ Database error")
```

**Metrics:**
- Products scraped per session
- AI analysis success rate
- Database operation counts

### 9.2 Proposed Monitoring
```
┌─────────────────────────────────────┐
│    Logging (Structured)             │
│  - ELK Stack / CloudWatch           │
│  - Error tracking                   │
│  - Performance metrics              │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│    Metrics (Time Series)            │
│  - Prometheus + Grafana             │
│  - Scraping throughput              │
│  - API latency                      │
│  - Database query time              │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│    Alerting                         │
│  - PagerDuty / Slack                │
│  - Scraping failures                │
│  - API quota exceeded               │
│  - Database connection loss         │
└─────────────────────────────────────┘
```

---

## 10. Disaster Recovery

### 10.1 Backup Strategy

**MongoDB Atlas:**
- Automated daily snapshots
- 7-day retention
- Point-in-time recovery (M10+)

**Code Repository:**
- Git version control
- GitHub remote backup
- Branch protection

**Configuration:**
- .env backed up separately (encrypted)
- Documentation in repository

### 10.2 Recovery Procedures

**Database Loss:**
1. Restore from MongoDB Atlas snapshot
2. Verify data integrity
3. Re-run scrapers for missing data
4. Regenerate reports

**Application Failure:**
1. Redeploy from Git repository
2. Restore .env file
3. Verify database connection
4. Test critical workflows

**Data Corruption:**
1. Identify affected products
2. Delete corrupted records
3. Re-scrape affected products
4. Validate data quality

---

## Appendix A: Technology Decision Matrix

| Requirement | Options Considered | Selected | Reason |
|-------------|-------------------|----------|--------|
| Web Framework | Flask, Django, Streamlit | **Streamlit** | Rapid prototyping, built-in UI |
| Database | PostgreSQL, MySQL, MongoDB | **MongoDB** | Flexible schema, array support |
| Web Scraping | Requests, Scrapy, Selenium | **Selenium** | JavaScript rendering support |
| AI Platform | OpenAI, Anthropic, Google | **Google Gemini** | Free tier, good quality |
| Multi-Agent | LangChain, AutoGPT, CrewAI | **CrewAI** | Specialized roles, task orchestration |
| PDF Library | FPDF, WeasyPrint, ReportLab | **ReportLab** | Professional quality, stable |

---

## Appendix B: Performance Benchmarks

| Operation | Current | Target | Notes |
|-----------|---------|--------|-------|
| Scrape 10 products | 30-45s | 15-20s | Parallel scraping |
| Quick AI analysis | 5-10s | 3-5s | Faster model |
| Deep AI analysis | 5-6 min | 2-3 min | Reduce delays |
| Database query | <100ms | <50ms | Better indexes |
| Dashboard load | 2-3s | <1s | Caching |
| PDF generation | 1-2s | <1s | Template optimization |

---

**Document Version:** 1.0  
**Last Updated:** February 15, 2026  
**Maintained By:** Development Team  
**Status:** Production Ready