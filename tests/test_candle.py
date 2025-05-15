import pytest 
from  fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.api.v1.candles.fetch_price_candles")
def test_get_candles_success(mock_fetch):
    # Arrange: mock return value
    mock_fetch.return_value = [
        {
            "timestamp": "2024-01-01T09:30:00Z",
            "open": 100.0,
            "high": 105.0,
            "low": 95.0,
            "close": 102.0,
            "volume": 100000
        }
    ]

    response = client.get("/api/v1/candles?symbol=AAPL&timeframe=1Day"
    "&start=2024-01-01T00:00:00&end=2024-01-10T00:00:00")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) ==1
    candle = data[0]
    assert candle["timestamp"] == "2024-01-01T09:30:00Z"
    assert candle["open"] == 100.0
    assert candle["high"] == 105.0
    assert candle["low"] == 95.0
    assert candle["close"] == 102.0
    assert candle["volume"] == 100000

