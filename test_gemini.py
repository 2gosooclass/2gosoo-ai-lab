import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
load_dotenv("/Users/2gosoo/Documents/2GOSOO_AI_LAB/.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment or .env file.")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

prompt = "Hello, tell me a joke in one line."

payload = {
    "contents": [{"parts": [{"text": prompt}]}]
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())
