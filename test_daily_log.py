import requests
import json

API_URL = "http://localhost:8000"

def test_daily_log():
    username = "TestUser_Logic"
    barcode = "123456789_LOG_TEST"
    
    print(f"Testing Daily Log for {username}...")
    
    # 1. Log a Meal
    payload = {
        "username": username,
        "barcode": barcode,
        "product_name": "Test Apple",
        "calories": 52.0,
        "quantity": 1.5, # 150g
        "status": "Green"
    }
    
    print(f"Logging meal: {payload}")
    try:
        resp = requests.post(f"{API_URL}/log/meal", json=payload)
        resp.raise_for_status()
        print(f"[SUCCESS] Log Response: {resp.json()}")
    except Exception as e:
        print(f"[FAILED] Log Meal: {e}")
        return

    # 2. Get Summary
    print(f"Fetching summary for {username}...")
    try:
        resp = requests.get(f"{API_URL}/log/summary/{username}")
        resp.raise_for_status()
        data = resp.json()
        print(f"[SUCCESS] Summary: {json.dumps(data, indent=2)}")
        
        # Verify calculations
        # Total calories = 52 * 1.5 = 78
        # Green = 100%, Red = 0%
        expected_cal = 78.0
        if abs(data['total_calories'] - expected_cal) < 1.0:
            print("[PASSED] Calorie calculation correct.")
        else:
            print(f"[FAILED] Calorie mismatch. Expected {expected_cal}, got {data['total_calories']}")
            
    except Exception as e:
        print(f"[FAILED] Get Summary: {e}")

if __name__ == "__main__":
    test_daily_log()
