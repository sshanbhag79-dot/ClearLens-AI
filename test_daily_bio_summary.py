import requests
import json
import time

API_URL = "http://localhost:8000"

def test_daily_summary_refactor():
    username = "TestUser_Summary"
    barcode = "999888777"
    
    print(f"Testing Daily Bio-Summary Refactor for {username}...")
    
    # 1. Log a Meal
    payload = {
        "username": username,
        "barcode": barcode,
        "product_name": "Test Burger",
        "calories": 500.0,
        "quantity": 1.0,
        "status": "Red"
    }
    
    print(f"Logging meal: {payload}")
    try:
        resp = requests.post(f"{API_URL}/log/meal", json=payload)
        resp.raise_for_status()
    except Exception as e:
        print(f"[FAILED] Log Meal: {e}")
        return

    # 2. Get Detailed History
    print(f"Fetching history for {username}...")
    try:
        resp = requests.get(f"{API_URL}/log/history/{username}")
        resp.raise_for_status()
        history = resp.json()
        print(f"[SUCCESS] History items: {len(history)}")
        print(json.dumps(history, indent=2))
        
        if len(history) > 0 and history[0]['product_name'] == "Test Burger":
            print("[PASSED] History retrieval correct.")
        else:
            print("[FAILED] History content mismatch.")
            
    except Exception as e:
        print(f"[FAILED] Get History: {e}")

if __name__ == "__main__":
    test_daily_summary_refactor()
