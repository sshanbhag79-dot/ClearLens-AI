import requests

API_URL = "http://localhost:8000"

def test_backend_logging():
    username = "BugTester"
    # Log something with 42.6 calories
    payload = {
        "username": username,
        "barcode": "5449000000996",
        "product_name": "Coke Test",
        "calories": 42.0,
        "quantity": 1.0,
        "status": "Red",
        "total_calories": 42.6
    }
    
    print(f"Logging: {payload}")
    resp = requests.post(f"{API_URL}/log/meal", json=payload)
    print(f"Response: {resp.status_code} - {resp.json()}")
    
    # Check Summary
    resp = requests.get(f"{API_URL}/log/summary/{username}")
    print(f"Summary: {resp.json()}")

if __name__ == "__main__":
    test_backend_logging()
