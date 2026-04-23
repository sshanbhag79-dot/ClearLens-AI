import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000"

def verify_meal_suggestions():
    print("--- Verifying Bio-Guide Meal Suggestions ---")
    
    # User Profile (Nut-Free, High Protein)
    profile = {
        "allergies": ["Nuts"],
        "diets": ["High Protein", "UPF-Free"],
        "strictness": "Strict"
    }

    # 1. Test Without Context (General Suggestion)
    print("\n[1] Testing General Suggestion (No context)...")
    payload1 = {
        "message": "I'm hungry, what should I eat for lunch?",
        "username": "BioTester",
        "barcode": None,
        "user_profile": profile
    }
    
    resp1 = requests.post(f"{API_URL}/chat/bio-guide", json=payload1)
    if resp1.status_code == 200:
        data = resp1.json()
        with open("meal_response.txt", "w", encoding="utf-8") as f:
            f.write(data['reply'])
        print("Response saved to meal_response.txt")
    else:
        print(f"Failed: {resp1.status_code} - {resp1.text}")

    # 2. Test With Context (Chicken Breast)
    print("\n[2] Testing Contextual Suggestion (Chicken Breast)...")
    payload2 = {
        "message": "What can I make with this chicken breast?",
        "username": "BioTester",
        "barcode": "5000212234567", # Mock barcode for chicken
        "user_profile": profile
    }
    
    # We call the API directly. Ensure the backend is running.
    # Note: The backend needs to be able to fetch "Chicken Breast" for this barcode or we pass it in.
    # For verification against the logic, we'll assume the API handles it.
    
    resp2 = requests.post(f"{API_URL}/chat/bio-guide", json=payload2)
    if resp2.status_code == 200:
        data = resp2.json()
        print(f"Bio-Guide: {data['reply']}")
    else:
        print(f"Failed: {resp2.status_code}")

if __name__ == "__main__":
    verify_meal_suggestions()
