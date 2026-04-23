import requests
import json

API_URL = "http://localhost:8000"

def verify_dashboard_flow():
    print("--- Verifying Dashboard & UPF Flow ---")
    username = "DashboardTester"
    
    # Clear history for clean test
    # (Actually we'll just use a suffix to avoid collisions in dev)
    import time
    user = f"Tester_{int(time.time())}"
    
    print(f"User: {user}")
    
    # 1. Log a Green item (100 kcal)
    print("\n1. Logging Green meal (100 kcal)...")
    requests.post(f"{API_URL}/log/meal", json={
        "username": user,
        "barcode": "111",
        "product_name": "Apple",
        "calories": 52.0,
        "quantity": 2.0, # ~104 kcal
        "status": "Green",
        "total_calories": 100.0
    })
    
    # 2. Log a Red item (300 kcal)
    print("2. Logging Red meal (300 kcal)...")
    requests.post(f"{API_URL}/log/meal", json={
        "username": user,
        "barcode": "666",
        "product_name": "Ultra-Processed Snack",
        "calories": 500.0,
        "quantity": 0.6,
        "status": "Red",
        "total_calories": 300.0
    })
    
    # Total = 400. Red = 300. Ratio = 300/400 = 75%.
    
    # 3. Fetch Summary
    print("\n3. Fetching Summary...")
    resp = requests.get(f"{API_URL}/log/summary/{user}")
    summary = resp.json()
    print(f"Summary: {summary}")
    
    # Verify
    expected_ratio = 75
    if summary["total_calories"] == 400 and summary["upf_ratio"] == expected_ratio:
        print("\n[PASSED] UPF Ratio and Total Calories are correct!")
    else:
        print("\n[FAILED] Calculation mismatch.")

if __name__ == "__main__":
    verify_dashboard_flow()
