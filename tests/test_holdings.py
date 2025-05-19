import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.db.models.investment import InvestmentPosition
from app.schemas.holdings import HoldingOut

client = TestClient(app)

def test_model_to_schema_contract():
    model = InvestmentPosition(
        id=999,
        symbol="TSLA",
        shares=1.0,
        purchase_price=100.0,
        purchase_date=datetime.utcnow(),
        current_price=110.0,
        auto_sell_triggered=False,
        created_at=datetime.utcnow()
    )

    schema = HoldingOut.model_validate(model)
    assert schema.symbol == "TSLA"
    assert schema.quantity == model.shares

def test_create_and_get_holding():
    create_payload = {
        "symbol": "APPL",
        "quantity": 10.5,
        "purchase_price": 145.00,
        "purchase_date": "2024-05-01T00:00:00"
    }

    create_response = client.post("/api/v1/holdings", json=create_payload)
    assert create_response.status_code == 200
    holding_data = create_response.json()
    assert holding_data["symbol"] == "APPL"
    assert holding_data["shares"] == 10.5
    holding_id = holding_data["id"]

    get_response = client.get(f"/api/v1/holdings/{holding_id}")
    assert get_response.status_code == 200
    retrieved = get_response.json()
    assert retrieved["id"] == holding_id
    assert retrieved["symbol"] == "APPL"

def test_get_all_holdings():
    response = client.get("/api/v1/holdings")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_holding():
    create_payload = {
        "symbol": "GOOG",
        "quantity": 8.0,
        "purchase_price": 120.0,
        "purchase_date": "2024-05-01T00:00:00"
    }
    create_response = client.post("/api/v1/holdings", json=create_payload)
    assert create_response.status_code == 200
    holding_id = create_response.json()["id"]

    update_payload = {
        "current_price": 130.0
    }
    update_response = client.put(f"/api/v1/holdings/{holding_id}", json=update_payload)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["current_price"] == 130.0

def test_delete_holding():
    create_payload = {
        "symbol": "NFLX",
        "quantity": 5.0,
        "purchase_price": 200.0,
        "purchase_date": "2024-05-01T00:00:00"
    }
    create_response = client.post("/api/v1/holdings", json=create_payload)
    assert create_response.status_code == 200
    holding_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/holdings/{holding_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"deleted": True}

    get_response = client.get(f"/api/v1/holdings/{holding_id}")
    assert get_response.status_code == 404
