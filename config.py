# config.py
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-1.5-flash')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

# Context management configuration
CONTEXT_DATA_DIR = "./context_data/"

# Ensure directories exist
os.makedirs(CONTEXT_DATA_DIR, exist_ok=True)