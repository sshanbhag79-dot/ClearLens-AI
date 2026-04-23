import requests

API_URL = "http://localhost:8000"

def verify_deletion():
    username = "DeletionTester"
    print(f"--- Verifying Deletion for {username} ---")
    
    # 1. Log a meal
    payload = {
        "username": username,
        "barcode": "123456",
        "product_name": "Delete Me",
        "calories": 100,
        "quantity": 1.0,
        "status": "Green",
        "total_calories": 100
    }
    
    log_resp = requests.post(f"{API_URL}/log/meal", json=payload)
    print(f"Log response: {log_resp.status_code}")
    
    # 2. Get history to find ID
    hist_resp = requests.get(f"{API_URL}/log/history/{username}")
    history = hist_resp.json()
    print(f"History count: {len(history)}")
    
    if history:
        log_id = history[0]['id']
        print(f"Deleting log ID: {log_id}")
        
        # 3. Delete the log
        del_resp = requests.delete(f"{API_URL}/log/{log_id}")
        print(f"Delete response: {del_resp.status_code}")
        
        # 4. Verify gone
        hist_resp_after = requests.get(f"{API_URL}/log/history/{username}")
        history_after = hist_resp_after.json()
        print(f"History count after delete: {len(history_after)}")
        
        if len(history_after) < len(history):
            print("✅ Deletion Verified!")
        else:
            print("❌ Deletion Failed!")

if __name__ == "__main__":
    verify_deletion()
