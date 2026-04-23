import requests
import json

url = "http://localhost:8000/scan"
payload = {
    "barcode": "5449000000996", # Coca Cola
    "user_profile": {
        "allergies": [],
        "diets": ["Low Sugar"],
        "strictness": "Strict"
    }
}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
