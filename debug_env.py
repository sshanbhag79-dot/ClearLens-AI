import os
from dotenv import load_dotenv

print(f"Current Working Directory: {os.getcwd()}")
load_dotenv(verbose=True)

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print(f"✅ GEMINI_API_KEY found: {api_key[:5]}... (length: {len(api_key)})")
else:
    print("❌ GEMINI_API_KEY not found.")
    print("Please ensure you have created a .env file with GEMINI_API_KEY=your_key")
