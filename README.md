# 🛒 AI Retail Intelligence System

An intelligent web scraping and analysis system that helps retailers make data-driven decisions by analyzing e-commerce product data from platforms like Amazon and Flipkart.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Features

### 🔍 **Web Scraping**
- Automated product data extraction from Amazon India
- Captures: product titles, prices, ratings, reviews, images
- Built with Selenium for reliability and JavaScript rendering support

### 🗄️ **Cloud Database**
- MongoDB Atlas cloud storage
- Organized collections for products, reports, and price history
- Scalable architecture for growing datasets

### 🤖 **AI-Powered Analysis**
- Powered by Google Gemini 2.5 Flash
- Generates actionable business insights
- Provides pricing strategies and competitive recommendations
- Analyzes market trends and identifies opportunities

### 📊 **Interactive Dashboard**
- Real-time data visualization with Streamlit
- 5 main sections:
  - **Home**: Overview and statistics
  - **Scrape Products**: Search and collect data
  - **Database Explorer**: View and filter products
  - **AI Analysis**: Generate insights
  - **Reports**: Historical analysis tracking

### 📄 **Professional PDF Reports**
- Download analysis reports as formatted PDFs
- Includes metrics, insights, and recommendations
- Ready to share with stakeholders

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Chrome browser (for Selenium)
- MongoDB Atlas account (free tier)
- Gemini API key (free from Google AI Studio)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/retail-ai-intelligence.git
cd retail-ai-intelligence
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
# API Keys
GROQ_API_KEY=your_groq_key_here
SERPAPI_KEY=your_serpapi_key_here
GEMINI_API_KEY=your_gemini_key_here

# MongoDB Atlas Connection
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/retail_intelligence

# Settings
SCRAPE_DELAY=2
MAX_RETRIES=3
```

**Get your API keys:**
- Gemini: https://aistudio.google.com/app/apikey
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas/register
- SerpAPI (optional): https://serpapi.com/

5. **Run the application**
```bash
venv\Scripts\Activate.ps1
```
```bash
python run_dashboard.py
```

The dashboard will open at `http://localhost:8501`

---

## 📖 Usage

### 1. Scraping Products

1. Navigate to **🔍 Scrape Products**
2. Enter a search query (e.g., "wireless headphones")
3. Set the number of products to scrape
4. Click **"Start Scraping"**
5. Data is automatically saved to MongoDB

### 2. Viewing Data

1. Go to **📊 View Database**
2. Use filters to narrow down results
3. View price distributions and statistics

### 3. AI Analysis

1. Navigate to **🤖 AI Analysis**
2. Select platform (Amazon/Flipkart)
3. Click **"Generate Analysis"**
4. View insights and download PDF report

### 4. Reports

- Access **📈 Reports** to view historical analyses
- Track trends over time
- Compare different analysis runs

---

## 🏗️ Project Structure
```
retail-ai-intelligence/
│
├── src/
│   ├── scrapers/
│   │   ├── base_scraper.py       # Base scraper class
│   │   └── amazon_scraper.py     # Amazon-specific scraper
│   │
│   ├── database/
│   │   └── mongo_manager.py      # MongoDB operations
│   │
│   ├── agents/
│   │   └── analysis_agent.py     # AI analysis logic
│   │
│   ├── utils/
│   │   ├── helpers.py            # Utility functions
│   │   └── pdf_generator.py      # PDF report generator
│   │
│   └── ui/
│       └── dashboard.py          # Streamlit dashboard
│
├── config/
│   └── settings.py               # Configuration management
│
├── data/                         # Local data storage
│
├── .env                          # Environment variables (not in git)
├── .gitignore
├── requirements.txt              # Python dependencies
├── run_dashboard.py              # Application launcher
└── README.md
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **Web Scraping** | Selenium, BeautifulSoup4 |
| **AI/LLM** | Google Gemini 2.5 Flash |
| **Database** | MongoDB Atlas |
| **UI Framework** | Streamlit |
| **PDF Generation** | ReportLab |
| **Data Processing** | Pandas, NumPy |

---

## 📊 Sample Output

### AI Analysis Report Includes:

- **Key Metrics**
  - Total products analyzed
  - Price range (min, max, average)
  
- **Top Rated Product**
  - Best product by customer rating
  
- **Best Value Product**
  - Most cost-effective option
  
- **Price Insights**
  - Market trends
  - Competitive positioning
  - Price gaps and opportunities
  
- **Strategic Recommendations**
  - Actionable business advice
  - Pricing strategies
  - Market opportunities

---

## 🔮 Future Enhancements

- [ ] Add Flipkart scraper
- [ ] Price tracking over time with charts
- [ ] Email alerts for price drops
- [ ] Sentiment analysis of customer reviews
- [ ] Multi-category support (clothing, groceries, etc.)
- [ ] Price prediction using ML
- [ ] Competitor comparison dashboards
- [ ] REST API for programmatic access
- [ ] Scheduled automatic scraping
- [ ] Image analysis with computer vision

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Selenium** for web automation
- **Google Gemini** for AI-powered analysis
- **MongoDB Atlas** for cloud database hosting
- **Streamlit** for the interactive dashboard framework
- **ReportLab** for PDF generation

---

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/retail-ai-intelligence](https://github.com/yourusername/retail-ai-intelligence)

---

## 🎓 Learning Resources

Built while learning:
- Web scraping with Python
- AI integration and prompt engineering
- NoSQL databases (MongoDB)
- Dashboard development with Streamlit
- PDF generation and reporting

---

**⭐ If you found this project helpful, please give it a star!**