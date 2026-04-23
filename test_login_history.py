
import os
import sys
import json
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/frontend")

# Mock streamlit before importing utils
import unittest.mock as mock
sys.modules["streamlit"] = mock.MagicMock()

from frontend.utils import save_user_history, load_user_history, HISTORY_FILE

def test_persistence():
    print("--- Testing User History Persistence ---")
    
    # 1. Clear existing history file for test
    if os.path.exists("frontend/" + HISTORY_FILE):
        os.remove("frontend/" + HISTORY_FILE)
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        
    username = "TestUser_Persistence"
    
    # 2. Verify empty initially
    history = load_user_history(username)
    print(f"Initial history: {len(history)} items")
    assert len(history) == 0
    
    # 3. Save a scan
    scan_item = {
        "barcode": "111222333",
        "product_name": "Test Product",
        "status": "Green",
        "timestamp": time.time()
    }
    print(f"Saving item for {username}...")
    save_user_history(username, scan_item)
    
    # 4. Load and verify
    loaded_history = load_user_history(username)
    print(f"Loaded history: {len(loaded_history)} items")
    assert len(loaded_history) == 1
    assert loaded_history[0]["barcode"] == "111222333"
    
    # 5. Check another user
    other_history = load_user_history("OtherUser")
    print(f"OtherUser history: {len(other_history)} items")
    assert len(other_history) == 0
    
    print("✅ Persistence Test Passed!")

if __name__ == "__main__":
    # Ensure CWD is correct for utils to find the file (utils expects file in CWD usually)
    # But utils.py was written to look for "user_history.json" in CWD.
    test_persistence()
