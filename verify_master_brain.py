import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000"

def test_chat(message, barcode=None, profile=None):
    payload = {
        "message": message,
        "username": "BioTester",
        "barcode": barcode,
        "user_profile": profile or {
            "allergies": [],
            "diets": ["High Protein", "UPF-Free"],
            "strictness": "Strict"
        }
    }
    resp = requests.post(f"{API_URL}/chat/bio-guide", json=payload)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {"error": resp.text}

def verify_master_reboot():
    print("--- Verifying Bio-Guide Master Brain Reboot ---")

    # 1. Test Decoding Health-Washing
    print("\n[1] Testing Decoder (Health-Washing)...")
    # Simulate a product with 'Natural' claim but 'E471' ingredient
    # We'll use a mock context if the API allows or just rely on the AI's response to the prompt.
    res1 = test_chat("This product says it's 'Natural' but it has E471 and Maltodextrin. What's the real story?")
    print(f"Bio-Guide: {res1.get('reply')[:200]}...")

    # 2. Test Bio-Chef with Pantry
    print("\n[2] Testing Bio-Chef (Pantry Combinations)...")
    res2 = test_chat("I have some chickpeas and spinach in my pantry. Can you suggest a meal using the chicken I just scanned?")
    print(f"Bio-Guide: {res2.get('reply')[:200]}...")

    # 3. Test Autonomous Logger (General Food)
    print("\n[3] Testing Autonomous Logger (General Food)...")
    res3 = test_chat("I just ate a large bowl of porridge with honey.")
    print(f"Bio-Guide: {res3.get('reply')[:200]}...")
    print(f"Intent detected: {res3.get('intent')}")
    print(f"Log Params: {res3.get('log_params')}")

    # 4. Test System Reboot Persona for Red Item
    print("\n[4] Testing System Reboot Persona (Red Item)...")
    res4 = test_chat("I'm eating a chocolate bar right now.")
    print(f"Bio-Guide: {res4.get('reply')[:200]}...")

if __name__ == "__main__":
    verify_master_reboot()
