from fastapi.testclient import TestClient
from backend.main import app
from backend.models import UserProfile
from unittest.mock import patch

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "BioFilter API is running"}

@patch("backend.routers.scan.get_product_by_barcode")
@patch("backend.routers.scan.analyze_safety")
def test_scan_endpoint(mock_analyze, mock_get_product):
    # Mock mocks
    mock_get_product.return_value = {
        "code": "123",
        "product_name": "Test Product",
        "ingredients_text": "Sugar, Water"
    }
    
    mock_analyze.return_value = {
        "status": "Red",
        "reason": "Too much sugar",
        "alternative": "Water",
        "product": {"code": "123", "product_name": "Test Product"}
    }
    
    payload = {
        "barcode": "123",
        "user_profile": {
            "allergies": ["Sugar"],
            "diets": [],
            "strictness": "Strict"
        }
    }
    
    response = client.post("/scan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Red"
    assert data["reason"] == "Too much sugar"
