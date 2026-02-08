
### 🛠️ Key Project Components

The instructor breaks down the project into several critical layers, from data gathering to the final user interface.

#### 1. Data Points and Categories

He emphasizes that the system should "think" like both a **retailer** and a **market researcher**. The focus is on collecting data across categories such as clothing, cosmetics, automobiles, and groceries. Key data points include:

* **Pricing:** Current prices, price drops over the last two months, and festive discounts.
* **Market Trends:** Trending products and consumer demand.
* **Competitive Analysis:** Identifying competitors and comparing their offerings on platforms like **Amazon, Flipkart, and Meesho**.
* **Logistics:** Location-based supply availability.

#### 2. The Technology Stack

The instructor recommends a specific set of tools to handle each stage of the project:

| Phase | Recommended Tools |
| --- | --- |
| **Data Extraction** | Serp API (search), Selenium (web scraping) |
| **Data Cleaning** | Pandas (Python library) |
| **AI Frameworks** | CrewAI, LangChain |
| **LLM Models** | Groq API, Claude API, Ollama, GPT-4 |
| **Databases** | MongoDB (unstructured), PostgreSQL/MySQL (structured), ChromaDB (vector storage for reports) |
| **Frontend/UI** | Streamlit |

---

### 🔄 Proposed Workflow

The instructor outlines a logical flow for how the AI agent should operate:

1. **Requirement Gathering:** Identify the trending products and competitive prices for a specific month.
2. **Web Scraping:** Extract raw HTML data and catalogs from competitor websites.
3. **Data Transformation:** Convert HTML tables into structured **JSON** format (which he explicitly prefers over CSV for agent compatibility).
4. **LLM Analysis:** Use AI models to extract insights like "cheapest price," "risk assessment," and "demand forecasting."
5. **Reporting:** Generate a summarized report and present it via a web interface.

---

### 💡 Core Insights for the Students

* **Persona-Driven Design:** Start by standing in the shoes of the end-user (retail manager) to understand what questions the data needs to answer.
* **Structured Storage:** Use different databases for different needs—ChromaDB is highlighted specifically for storing reports and summaries.
* **JSON over CSV:** He advises using JSON for data exchange because it is more robust for AI agents to process.



---


🚀 Recommended Next Steps (Priority Order)
Phase 1: Core Missing Features (Must Have)
1. Add Multiple Platforms 🔥 CRITICAL

*Build Flipkart scraper
*Build Meesho scraper (if possible)
*Enable platform comparison

2. Price Tracking Over Time 🔥 CRITICAL

*Store price history in price_history collection
*Track changes over 2 months
*Detect price drops
*Show trend charts

3. Multiple Categories 🔥 CRITICAL

*Add: Clothing, Cosmetics, Groceries, Automobiles
*Category-specific scraping logic
*Category filtering in dashboard

4. Competitive Analysis 🔥 CRITICAL

*Side-by-side platform comparison
*"Cheapest price" finder
*Platform pricing strategies


Phase 2: Advanced Features (Should Have)
5. Trending Products Detection

*Use SerpAPI to find trending searches
*Track product popularity
*Consumer demand signals

6. Festive Discount Tracking

*Detect discount patterns
*Compare festive vs regular prices
*Alert on special offers

7. AI Risk Assessment

*Analyze pricing risks
*Stock availability risks
*Market saturation analysis

8. Demand Forecasting

*Predict future demand
*Seasonal trends
*Purchase recommendations


Phase 3: Nice to Have
9. ChromaDB for Vector Storage

*Store reports as embeddings
*Semantic search through reports
*Better report retrieval

10. Location-based Analysis

*Track regional availability
*Logistics insights
*Delivery time analysis