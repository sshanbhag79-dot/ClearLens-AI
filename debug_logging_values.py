import requests
import json

API_URL = "http://localhost:8000"

def debug_scan_values(barcode):
    print(f"--- Debugging Scan Values for {barcode} ---")
    
    payload = {
        "barcode": barcode,
        "user_profile": {
            "allergies": [],
            "diets": [],
            "strictness": "Strict"
        }
    }
    
    try:
        response = requests.post(f"{API_URL}/scan", json=payload)
        response.raise_for_status()
        result = response.json()
        
        product = result.get('product', {})
        calories = product.get('calories')
        quantity_val = product.get('quantity_val')
        
        print(f"Product: {product.get('product_name')}")
        print(f"Calories (kcal/100g): {calories}")
        print(f"Quantity Val: {quantity_val}")
        
        if quantity_val:
            scanned_calories = (quantity_val / 100.0) * (calories or 0)
        else:
            scanned_calories = (calories or 0)
            
        print(f"Calculated Scanned Calories (per unit): {scanned_calories}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test with a common product (Coca Cola 330ml)
    # 5449000000996 is Coke
    debug_scan_values("5449000000996")
    # Test with Pepsi Max (0 cal)
    debug_scan_values("5449000133335") 
