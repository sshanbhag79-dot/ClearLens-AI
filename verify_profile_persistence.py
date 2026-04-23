import requests
import json
import time

API_URL = "http://localhost:8000"

def verify_profile_persistence():
    print("--- Verifying Profile Persistence ---")
    username = "PersistenceTester"
    
    # 1. Initial State (Expect empty or default)
    print(f"\n1. Fetching initial profile for {username}...")
    resp = requests.get(f"{API_URL}/user/{username}")
    initial_profile = resp.json()
    print(f"Initial: {initial_profile}")
    
    # 2. Update Profile
    new_profile = {
        "allergies": ["Peanuts", "Dairy"],
        "diets": ["Keto", "High-Protein"],
        "strictness": "Strict"
    }
    print(f"\n2. Updating profile to: {new_profile}...")
    resp = requests.post(f"{API_URL}/user/{username}", json=new_profile)
    if resp.status_code == 200:
        print("[SUCCESS] Update API call successful.")
    else:
        print(f"[FAIL] Update API call failed: {resp.status_code}")
        return

    # 3. Verify Persistence (Fetch again)
    print(f"\n3. Fetching profile again to verify persistence...")
    resp = requests.get(f"{API_URL}/user/{username}")
    verified_profile = resp.json()
    print(f"Verified: {verified_profile}")
    
    if verified_profile == new_profile:
        print("\n[PASSED] Profile persisted correctly in Database!")
    else:
        print("\n[FAILED] Profile mismatch or not persisted.")

if __name__ == "__main__":
    verify_profile_persistence()
