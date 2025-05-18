import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_holding():
    # Step 1: Ceate a holding
    create_payload = {
        "symbol": "APPL",
        "quantity": 10.5,
        "purchase_price": 145.00,
        "purchase_date": "2024-05-01T00:00:00"
    }

    create_response = client.post("/api/v1/holdings", json=create_payload)
    print("Response Status Code:", create_response.status_code)
    print("Response JSON:", create_response.json())
    assert create_response.status_code == 200
    holding_data = create_response.json()
    assert holding_data["symbol"] == "APPL"
    assert holding_data["shares"] == 10.5

    holding_id = holding_data["id"]

    # Step 2: Retrieve the holding by ID
    get_response = client.get(f"/api/v1/holdings/{holding_id}")
    assert get_response.status_code == 200
    retrieved = get_response.json()
    assert retrieved["id"] == holding_id
    assert retrieved["symbol"] == "APPL"