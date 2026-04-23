import requests

API_URL = "http://localhost:8000"

def verify_bio_guide():
    print("--- Verifying Bio-Guide AI ---")
    
    # 1. Test Ingredient Translation
    payload_chat = {
        "message": "What is Maltodextrin?",
        "username": "BioTester",
        "barcode": "5449000000996", # Coke
        "user_profile": {"allergies": [], "diets": [], "strictness": "Flexible"}
    }
    
    chat_resp = requests.post(f"{API_URL}/chat/bio-guide", json=payload_chat)
    if chat_resp.status_code == 200:
        data = chat_resp.json()
        print(f"Reply: {data['reply']}")
    else:
        print(f"Chat failed: {chat_resp.status_code}")

    # 2. Test Logging Intent
    payload_log = {
        "message": "I just ate half of this product. Log it.",
        "username": "BioTester",
        "barcode": "5449000000996",
        "user_profile": {"allergies": [], "diets": [], "strictness": "Flexible"}
    }
    
    log_intent_resp = requests.post(f"{API_URL}/chat/bio-guide", json=payload_log)
    if log_intent_resp.status_code == 200:
        data = log_intent_resp.json()
        print(f"Intent detected: {data.get('intent')}")
        print(f"Log Params: {data.get('log_params')}")
        if data.get('intent') == "LOG_MEAL":
            print("✅ Intent Detection Verified!")
        else:
            print("❌ Intent Detection Failed!")
    else:
        print(f"Chat intent failed: {log_intent_resp.status_code}")

if __name__ == "__main__":
    verify_bio_guide()
