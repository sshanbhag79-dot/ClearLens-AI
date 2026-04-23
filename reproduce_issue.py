
import requests
import json

API_URL = "http://localhost:8000"

payload = {
    "barcode": "4060800104045",  # Pepsi Max
    "user_profile": {
        "allergies": [],
        "diets": [],
        "strictness": "Strict"
    }
}

try:
    print(f"Sending request to {API_URL}/scan...")
    response = requests.post(f"{API_URL}/scan", json=payload)
    response.raise_for_status()
    data = response.json()
    
    print("\n--- API Response ---")
    # print(json.dumps(data, indent=2))
    
    print(f"Status: {data.get('status')}")
    print(f"Marketing vs Reality: {data.get('marketing_vs_reality')}")
    print(f"Trust Verdict: {data.get('trust_score')}/10")
    print(f"Community Takeaway: {data.get('community_takeaway')}")
    print(f"Bio Red Flags: {data.get('bio_red_flags')}")
    
    product = data.get("product", {})
    print(f"Product Calories (Parsed): {product.get('calories')} kcal/100g")
    
    # DEBUG: Fetch raw data to inspect quantity/serving size
    try:
        barcode = payload["barcode"]
        raw_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        raw_resp = requests.get(raw_url, timeout=5)
        raw_data = raw_resp.json()
        p_raw = raw_data.get("product", {})
        
        print("\n--- Raw Quantity Data ---")
        print(f"product_quantity: {p_raw.get('product_quantity')}")
        print(f"quantity: {p_raw.get('quantity')}")
        print(f"serving_size: {p_raw.get('serving_size')}")
        print(f"serving_quantity: {p_raw.get('serving_quantity')}")
        
    except Exception as e:
        print(f"Failed to fetch raw data: {e}")
    
    if "ingredients_analysis" in data:
        print(f"\nIngredients Found: {len(data['ingredients_analysis'])}")
    else:
        print("\nMISSING 'ingredients_analysis' key!")

except Exception as e:
    print(f"Error: {e}")
