import requests
import json

API_URL = "http://localhost:8000"

def inspect_raw_scan(barcode):
    payload = {
        "barcode": barcode,
        "user_profile": {"allergies": [], "diets": [], "strictness": "Strict"}
    }
    resp = requests.post(f"{API_URL}/scan", json=payload)
    print(json.dumps(resp.json(), indent=2))

if __name__ == "__main__":
    inspect_raw_scan("5449000000996") # Coke
