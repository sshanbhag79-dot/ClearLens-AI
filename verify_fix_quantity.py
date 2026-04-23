import requests
import json

API_URL = "http://localhost:8000"

def verify_fix():
    print("Verifying Quantity vs Calories Fix...")
    
    # Simulate logging 1 can of Pepsi Max (330ml, 0.4 kcal/100ml)
    # Expected: Quantity = 1, Total Calories = 1.32
    
    username = "TestUser_Fix"
    barcode = "4060800104045"
    product_name = "Pepsi Max (Fix Test)"
    calories_per_100g = 0.4
    quantity_units = 1.0 # 1 Unit
    
    # Calculate expected total
    unit_size = 330
    total_grams = quantity_units * unit_size
    expected_total_cals = (total_grams / 100.0) * calories_per_100g
    
    print(f"Logging: {quantity_units} unit(s) of 330ml (0.4 kcal/100g)")
    print(f"Calculated Total Cals: {expected_total_cals}")
    
    payload = {
        "username": username,
        "barcode": barcode,
        "product_name": product_name,
        "calories": calories_per_100g,
        "quantity": quantity_units, # sending "1"
        "status": "Yellow",
        "total_calories": expected_total_cals # sending explicit total
    }
    
    try:
        # Log it
        resp = requests.post(f"{API_URL}/log/meal", json=payload)
        resp.raise_for_status()
        print("[SUCCESS] Logged meal.")
        
        # Check History
        resp = requests.get(f"{API_URL}/log/history/{username}")
        history = resp.json()
        
        if not history:
            print("[FAIL] No history found.")
            return

        latest = history[0]
        print("\n--- Latest Log Entry ---")
        print(f"Product: {latest['product_name']}")
        print(f"Quantity: {latest['quantity']}")
        print(f"Calories Total: {latest['calories_total']}")
        
        # Verify
        if latest['quantity'] == 1.0 and abs(latest['calories_total'] - expected_total_cals) < 0.1:
            print("[PASSED] Quantity is 1.0 and Calories Total is correct.")
        else:
            print("[FAILED] Values mismatch.")
            
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    verify_fix()
