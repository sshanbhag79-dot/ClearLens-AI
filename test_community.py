
import os
import sys
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from backend.main import app
from backend import community_db

# Initialize DB for testing
community_db.init_db()

def test_community_flow():
    print("--- Testing Community API Link (5-Star System) ---")
    barcode = "123456789_RATING_TEST"
    
    # 1. Clean up previous test data
    conn = community_db.get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM flags WHERE barcode = ?", (barcode,))
    conn.commit()
    conn.close()
    
    # 2. Simulate votes
    print("Seeding test ratings...")
    # Avg should be (5+1+5)/3 = 3.66 -> 3.7
    community_db.save_vote(barcode, 5, "Amazing!", "UserA")
    community_db.save_vote(barcode, 1, "Terrible.", "UserB")
    community_db.save_vote(barcode, 5, "Love it.", "UserC")
    
    # 3. Call the Endpoint
    client = TestClient(app)
    print(f"Fetching data for {barcode}...")
    try:
        response = client.get(f"/community/{barcode}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return

        data = response.json()
        print("Response Data:", json.dumps(data, indent=2))
        
        # 4. Verify Data
        assert data["barcode"] == barcode
        assert data["total_reviews"] == 3
        assert data["average_rating"] == 3.7
        assert len(data["recent_reviews"]) >= 3
        
        # Verify username presence
        assert "username" in data["recent_reviews"][0]
        print(f"Verified Username: {data['recent_reviews'][0]['username']}")
        
        print("✅ Community API + 5-Star Rating + Usernames Verified!")
        
    except Exception as e:
        print(f"❌ Test Failed: {e}")

if __name__ == "__main__":
    test_community_flow()
