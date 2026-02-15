# Retail Intelligence Platform

![CI/CD Status](https://github.com/Nikhilgarg0/retail-ai-intelligence/workflows/Retail%20Intelligence%20CI%2FCD/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

AI-Powered competitive intelligence and market analysis platform for e-commerce retailers.


# 🛒 AI-Powered Retail Intelligence Platform

> Automated competitive intelligence and market analysis for retail businesses

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Screenshots](#screenshots)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)

---

## 🎯 Overview

The **AI-Powered Retail Intelligence Platform** is an end-to-end solution that automates competitive intelligence gathering, price tracking, and market analysis for retail businesses. It leverages web scraping, cloud databases, and AI agents to provide actionable insights.

### Business Problem

Retail businesses struggle with:
- ⏰ **Time-consuming manual price monitoring**
- 🔍 **Lack of real-time competitive intelligence**
- 📊 **Difficulty tracking multi-platform pricing**
- 💡 **Limited data-driven decision making**

### Our Solution

- ✅ **Automated multi-platform scraping** (Amazon, Flipkart)
- ✅ **Intelligent price tracking** with historical analysis
- ✅ **AI-powered insights** (single-agent + multi-agent systems)
- ✅ **Professional dashboard** for visualization
- ✅ **Exportable PDF reports**

---

## ✨ Key Features

### 🔍 Data Collection
- **Multi-platform scraping**: Amazon India, Flipkart
- **Smart product tracking**: Unique ID-based deduplication
- **Automatic categorization**: Electronics, Clothing, Cosmetics, etc.
- **Real-time updates**: Track price changes as they happen

### 📊 Price Intelligence
- **Historical price tracking**: Track price changes over time
- **Trend analysis**: Identify upward/downward price movements
- **Price drop alerts**: Discover opportunities for competitive pricing
- **Cross-platform comparison**: Compare prices across marketplaces

### 🤖 AI-Powered Analysis

#### Quick Analysis (5-10 seconds)
- Single AI agent using Google Gemini
- Price range analysis
- Top-rated products
- Best value recommendations

#### Deep Analysis (5-6 minutes)
- Multi-agent CrewAI system with 5 specialized agents:
  - 🔍 **Data Scout**: Market trends and gaps
  - 💰 **Pricing Strategist**: Pricing optimization
  - ⚠️ **Risk Assessor**: Market risks and threats
  - 📈 **Demand Forecaster**: Future demand predictions
  - 📝 **Report Writer**: Executive summaries

### 📱 Professional Dashboard
- Clean, modern interface
- Real-time metrics and KPIs
- Interactive data explorer
- Price analytics visualizations
- Report management

### 📄 Reporting
- Professional PDF generation
- Downloadable analysis reports
- Historical report archive
- Custom formatting

---

## 🏗️ System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────┐
│              USER INTERFACE LAYER                       │
│         (Streamlit Professional Dashboard)              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              APPLICATION LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Scrapers   │  │  AI Agents   │  │   Reports    │  │
│  │  - Amazon    │  │  - Gemini    │  │  - PDF Gen   │  │
│  │  - Flipkart  │  │  - CrewAI    │  │  - Export    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              DATA LAYER                                 │
│         MongoDB Atlas (Cloud Database)                  │
│  - Products  - Price History  - Reports                │
└─────────────────────────────────────────────────────────┘
```

![System Architecture](docs/diagrams/system_architecture.png)

### Data Flow

![Data Flow](docs/diagrams/data_flow.png)

### Multi-Agent System

![Multi-Agent System](docs/diagrams/multi_agent.png)

**See full architecture documentation**: [docs/LLD.md](docs/LLD.md)

---

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.11+ | Core development |
| **Web Scraping** | Selenium, BeautifulSoup4 | Data extraction |
| **AI/LLM** | Google Gemini 2.5 Flash | Quick analysis |
| **Multi-Agent** | CrewAI, Groq (Llama 3.3) | Deep analysis |
| **Database** | MongoDB Atlas | Cloud storage |
| **UI Framework** | Streamlit | Dashboard |
| **PDF Generation** | ReportLab | Report creation |
| **Data Processing** | Pandas, NumPy | Data manipulation |

### External Services
- **MongoDB Atlas**: Cloud NoSQL database (M0 Free Tier)
- **Google AI Studio**: Gemini API access
- **Groq Cloud**: Alternative LLM API
- **E-commerce Sites**: Amazon.in, Flipkart.com

---

## 🚀 Installation

### Prerequisites

1. **Python 3.11+**
```powershell
   python --version
```

2. **Google Chrome** (for Selenium)

3. **MongoDB Atlas Account** (free tier)
   - Sign up at: https://www.mongodb.com/cloud/atlas/register

4. **Gemini API Key** (free)
   - Get from: https://aistudio.google.com/app/apikey

### Setup Steps

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/retail-ai-intelligence.git
   cd retail-ai-intelligence
```

2. **Create virtual environment**
```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   # source venv/bin/activate    # Mac/Linux
```

3. **Install dependencies**
```powershell
   pip install -r requirements.txt
```

4. **Configure environment variables**

   Create `.env` file:
```env
   GROQ_API_KEY=your_groq_key
   GEMINI_API_KEY=your_gemini_key
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/retail_intelligence
```

5. **Run the application**
```powershell
   python run_dashboard.py
```

6. **Access dashboard**
   - Open browser: http://localhost:8501

---

## 📱 Usage

### 1. Collect Data

1. Navigate to **Data Collection** in sidebar
2. Enter product search query (e.g., "wireless headphones")
3. Select platform (Amazon or Flipkart)
4. Choose category
5. Click "Start Collection"

### 2. Explore Products

1. Go to **Product Explorer**
2. Use filters (platform, category, view mode)
3. Click on products for detailed tracking data
4. View price history charts

### 3. Analyze Data

**Quick Analysis:**
1. Go to **AI Insights**
2. Select "Quick Analysis"
3. Choose platform
4. Click "Generate Analysis"
5. Download PDF report

**Deep Analysis:**
1. Select "Deep Analysis (Multi-Agent)"
2. Wait 5-6 minutes for multi-agent collaboration
3. View detailed agent outputs

### 4. Track Prices

1. Navigate to **Price Analytics**
2. View price drops, increases, and distribution
3. Set minimum drop percentage filter
4. Identify opportunities

---

## 📂 Project Structure
```
retail-ai-intelligence/
├── src/
│   ├── scrapers/              # Web scraping modules
│   │   ├── base_scraper.py
│   │   ├── amazon_scraper.py
│   │   └── flipkart_scraper.py
│   ├── database/              # Database operations
│   │   └── mongo_manager.py
│   ├── agents/                # AI agents
│   │   ├── analysis_agent.py  # Single agent
│   │   └── crew_manager.py    # Multi-agent system
│   ├── utils/                 # Utilities
│   │   ├── helpers.py
│   │   └── pdf_generator.py
│   └── ui/
│       └── dashboard.py       # Streamlit dashboard
├── config/
│   └── settings.py            # Configuration
├── docs/                      # Documentation
│   ├── LLD.md                # Low-level design
│   ├── diagrams/             # Architecture diagrams
│   └── generate_diagrams.py
├── data/                      # Local data storage
├── .env                       # Environment variables
├── requirements.txt           # Dependencies
├── README.md
└── run_dashboard.py          # Application launcher
```

---

## 📚 Documentation

- **[Low-Level Design (LLD)](docs/LLD.md)**: Complete technical documentation
- **[Architecture Diagrams](docs/diagrams/)**: Visual system design
- **[API Documentation](docs/API.md)**: Coming soon

---

## 📸 Screenshots

### Dashboard Home
![Dashboard](docs/screenshots/dashboard.png)
*Professional dashboard with key metrics and quick actions*

### Data Collection
![Scraping](docs/screenshots/scraping.png)
*Multi-platform data collection interface*

### AI Analysis
![AI Insights](docs/screenshots/ai_analysis.png)
*AI-powered market analysis and recommendations*

### Price Analytics
![Price Tracking](docs/screenshots/price_analytics.png)
*Price drop detection and trend analysis*

---

## 🗺️ Future Roadmap

### Phase 1: Enhanced Features (Next 1-2 months)
- [ ] Add Meesho scraper
- [ ] Email alerts for price drops
- [ ] Scheduled automated scraping
- [ ] Advanced filtering and search

### Phase 2: Advanced Analytics (2-4 months)
- [ ] Machine learning price prediction
- [ ] Sentiment analysis of reviews
- [ ] Market share analysis
- [ ] Competitive benchmarking

### Phase 3: Scale & Deploy (4-6 months)
- [ ] RESTful API development
- [ ] Multi-user support
- [ ] Role-based access control
- [ ] Docker containerization
- [ ] Kubernetes deployment

### Phase 4: Intelligence (6+ months)
- [ ] Recommendation engine
- [ ] Anomaly detection
- [ ] Custom ML models
- [ ] Real-time streaming data

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**[Your Name]**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **Google Gemini** for AI capabilities
- **CrewAI** for multi-agent framework
- **MongoDB** for database infrastructure
- **Streamlit** for rapid UI development
- Instructor **[Instructor Name]** for project guidance

---

## 📊 Project Stats

- **Lines of Code**: ~3,500+
- **Python Files**: 15+
- **Test Coverage**: In progress
- **Database Collections**: 2
- **AI Agents**: 6 (1 single + 5 multi-agent)
- **Supported Platforms**: 2 (Amazon, Flipkart)
- **Categories**: 5

---

## 🔗 Quick Links

- [Installation Guide](#installation)
- [Usage Guide](#usage)
- [Architecture Documentation](docs/LLD.md)
- [API Reference](docs/API.md) (Coming soon)
- [Deployment Guide](docs/DEPLOYMENT.md) (Coming soon)

---

**Built with ❤️ using Python, AI, and Cloud Technologies**

*Last Updated: February 15, 2026*