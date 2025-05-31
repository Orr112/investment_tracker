import pytest 
from datetime import datetime 
from fastapi.testclient import TestClient
from sqlalchemy.orm import session
from app.main import app
from app.db.database import get_db
from app.db.models.pricing import PriceCandle as CandleModel

client = TestClient(app)

@pytest.fixture(scope="module")
def test_candle_payload():
    return {
        "symbol": "TSLA",
        "timestamp": "2024-01-01T00:00:00",
        "open": 100.0,
        "high": 110.0,
        "low": 95.0,
        "close": 105.0,
        "volume": 500000
    }

def test_create_candle(test_candle_payload):
    response = client.post("/api/v1/candles", json=test_candle_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == test_candle_payload["symbol"]
    assert data["close"] == test_candle_payload["close"]

def test_read_candles():
    response = client.get("/api/v1/candles/db?symbol=TSLA")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(candle["symbol"] == "TSLA" for candle in data)

def test_update_candle():
    # Fetch existing to get ID
    candles = client.get("/api/v1/candles/db?symbol=TSLA").json()
    candle_id = candles[0]["id"]

    update_payload = {"close": 107.5}
    response = client.put(f"/api/v1/candles/{candle_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["close"]  == 107.5

def test_delete_candle():
    # Fetch existing to get ID
    candles = client.get("/api/v1/candles/db?symbol=TSLA").json()
    candle_id = candles[0]["id"]

    response = client.delete(f"/api/v1/candles/{candle_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"