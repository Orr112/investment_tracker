import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

# ✅ Shared mock response data
mock_bar_data = [
    {
        "timestamp": "2024-01-01T00:00:00Z",
        "open": 150.0,
        "high": 155.0,
        "low": 149.0,
        "close": 153.0,
        "volume": 1000000
    }
]

# ✅ GET endpoint test (return candles)
@patch("app.api.v1.candles.fetch_price_candles")
def test_get_candles_success(mock_fetch):
    mock_fetch.return_value = mock_bar_data

    response = client.get("/api/v1/candles", params={
        "symbol": "AAPL",
        "timeframe": "1Day",
        "start": "2024-01-01T00:00:00",
        "end": "2024-01-10T00:00:00"
    })

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["open"] == 150.0
    assert data[0]["high"] == 155.0
    assert data[0]["low"] == 149.0
    assert data[0]["close"] == 153.0
    assert data[0]["volume"] == 1000000

# ✅ POST endpoint test (store candles)
@patch("app.api.v1.candles.store_candles")
@patch("app.api.v1.candles.fetch_price_candles")
def test_ingest_candles(mock_fetch, mock_store):
    mock_fetch.return_value = mock_bar_data
    mock_store.return_value = None

    response = client.post("/api/v1/candles/AAPL")

    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "ingested"
    assert result["count"] == 1
    mock_store.assert_called_once()
