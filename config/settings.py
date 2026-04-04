from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # API Keys
    groq_api_key: str
    serpapi_key: Optional[str] = None
    gemini_api_key: str  # Changed from anthropic

    # Database - MongoDB Atlas
    mongodb_uri: str
    chroma_path: str = "./data/chroma_db"

    # Scraping Settings
    scrape_delay: int = 2
    max_retries: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
try:
    settings = Settings()
    # Bridge keys into os.environ so CrewAI/litellm can read them
    os.environ.setdefault("GROQ_API_KEY", settings.groq_api_key or "")
    os.environ.setdefault("GEMINI_API_KEY", settings.gemini_api_key or "")
    print("✅ Settings loaded successfully!")
except Exception as e:
    print(f"❌ Error loading settings: {e}")
    print("Make sure your .env file has all required keys!")
