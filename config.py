# config.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file if it exists
load_dotenv()

# LLM provider settings (will be replaced with real later)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "dummy")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "dummy-model")

# API keys (placeholders for later)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Brand configuration for Mediterraneo Tropical
BRAND_NAME = "Mediterraneo Tropical"
