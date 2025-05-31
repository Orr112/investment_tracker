
import pytest
from datetime import datetime

def test_create_candle(client, db_session):
    payload = {
        
        "symbol": "AAPL",
        "open": 190.5,
        "high": 192.1,
        "low": 189.3,
        "close": 191.8,
        "volume": 50234123,
        "timestamp": datetime.utcnow().isoformat()
    }

    response = client.post("/api/v1/candles-debug", json=payload)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == payload["symbol"]
    assert "id" in data
