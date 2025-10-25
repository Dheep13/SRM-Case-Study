"""Configuration module for GenAI Learning & Trend Analysis Agents."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Model Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# Agent Configuration
MAX_SEARCH_RESULTS = 10
MAX_TREND_ITEMS = 15
CONTENT_TYPES = ["tutorial", "course", "article", "video", "documentation"]

# API Endpoints
GITHUB_TRENDING_URL = "https://api.github.com/search/repositories"
GITHUB_TOPICS_URL = "https://api.github.com/search/topics"

def validate_config():
    """Validate that required configuration is present."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required. Please set it in .env file.")
    
    if not TAVILY_API_KEY:
        print("Warning: TAVILY_API_KEY not set. Web search functionality may be limited.")
    
    return True



