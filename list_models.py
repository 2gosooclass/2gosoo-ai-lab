import os
import requests
from dotenv import load_dotenv

load_dotenv()
load_dotenv("/Users/2gosoo/Documents/2GOSOO_AI_LAB/.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment or .env file.")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"

response = requests.get(url)
print(response.status_code)
print(response.json())
