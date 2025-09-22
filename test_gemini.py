import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Hello, test message")
        print("✅ Gemini API working!")
        print(response.text)
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
else:
    print("❌ No API key found")