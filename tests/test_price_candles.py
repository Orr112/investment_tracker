import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime, timedelta

from app.db.models.pricing import PriceCandle as CandleModel
from app.schemas.pricing import PriceCandleCreate

# -------------------------------
# 🔹 Test: Debug/Create Candle
# -------------------------------
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
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == payload["symbol"]
    assert "id" in data


# -------------------------------
# 🔹 Test: Ingest from API
# -------------------------------
def test_ingest_candles(client, db_session):
    mocked_bars = [
        {"t": datetime(2024, 1, 2, 10, 0, 0), "o": 100, "h": 110, "l": 95, "c": 105, "v": 150000},
        {"t": datetime(2024, 1, 3, 10, 0, 0), "o": 106, "h": 112, "l": 100, "c": 108, "v": 130000}
    ]
    with patch("app.api.v1.candles.fetch_price_candles", return_value=mocked_bars):
        response = client.post("/api/v1/candles/TEST")

        assert response.status_code == 200
        assert response.json()["status"] == "ingested"
        assert response.json()["count"] == 2

        candles = db_session.query(CandleModel).filter_by(symbol="TEST").all()
        assert len(candles) == 2


# -------------------------------
# 🔹 Test: Read All by Symbol
# -------------------------------
def test_read_candles(client, db_session):
    candle = CandleModel(**PriceCandleCreate(
        symbol="TSLA",
        open=800.0, high=820.0, low=790.0, close=810.0,
        volume=32100000,
        timestamp=datetime.utcnow() - timedelta(days=1)
    ).dict())

    db_session.add(candle)
    db_session.commit()
    db_session.refresh(candle)

    response = client.get("/api/v1/candles/db", params={"symbol": "TSLA"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["symbol"] == "TSLA" for item in data)


# -------------------------------
# 🔹 Test: Read by ID
# -------------------------------
def test_get_price_candle_by_id(client, db_session):
    candle = CandleModel(**PriceCandleCreate(
        symbol="NFLX",
        open=400.0, high=410.0, low=390.0, close=405.0,
        volume=17000000,
        timestamp=datetime.utcnow() - timedelta(days=1)
    ).dict())
    db_session.add(candle)
    db_session.commit()
    db_session.refresh(candle)

    response = client.get(f"/api/v1/candles/{candle.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == candle.id
    assert data["symbol"] == candle.symbol


# -------------------------------
# 🔹 Test: Read with Date Filtering
# -------------------------------
def test_read_candles_with_date_filtering(client, db_session):
    now = datetime.utcnow()

    candle1 = CandleModel(**PriceCandleCreate(
        symbol="MSFT", open=300.0, high=310.0, low=295.0, close=305.0,
        volume=15000000, timestamp=now - timedelta(days=3)
    ).dict())

    candle2 = CandleModel(**PriceCandleCreate(
        symbol="MSFT", open=310.0, high=320.0, low=305.0, close=315.0,
        volume=16000000, timestamp=now - timedelta(days=1)
    ).dict())

    db_session.add_all([candle1, candle2])
    db_session.commit()

    start = (now - timedelta(days=2)).isoformat()
    response = client.get(f"/api/v1/candles/db?symbol=MSFT&start={start}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    end = (now - timedelta(days=2)).isoformat()
    response = client.get(f"/api/v1/candles/db?symbol=MSFT&end={end}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    start = (now - timedelta(days=4)).isoformat()
    end = now.isoformat()
    response = client.get(f"/api/v1/candles/db?symbol=MSFT&start={start}&end={end}")
    assert response.status_code == 200
    assert len(response.json()) == 2


# -------------------------------
# 🔹 Test: Get All Symbols
# -------------------------------
def test_get_all_symbols(client, db_session):
    # Clean up to avoid leftovers from other tests
    db_session.query(CandleModel).delete()
    db_session.commit()

    db_session.add_all([
        CandleModel(symbol="AAPL", open=100, high=105, low=95, close=102, volume=1000000, timestamp=datetime.utcnow()),
        CandleModel(symbol="MSFT", open=200, high=210, low=190, close=202, volume=2000000, timestamp=datetime.utcnow())
    ])
    db_session.commit()

    response = client.get("/api/v1/symbols")
    assert response.status_code == 200
    assert set(response.json()) == {"AAPL", "MSFT"}



# -------------------------------
# 🔹 Test: Update Candle
# -------------------------------
def test_update_candle(client, db_session):
    candle = CandleModel(**PriceCandleCreate(
        symbol="AMZN",
        open=100.0, high=105.0, low=98.0, close=102.0,
        volume=10000000, timestamp=datetime.utcnow()
    ).dict())

    db_session.add(candle)
    db_session.commit()
    db_session.refresh(candle)

    update_data = {"close": 103.5, "volume": 11000000}
    response = client.put(f"/api/v1/candles/{candle.id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["close"] == update_data["close"]
    assert data["volume"] == update_data["volume"]


# -------------------------------
# 🔹 Test: Delete Candle
# -------------------------------
def test_delete_candle(client, db_session):
    candle = CandleModel(**PriceCandleCreate(
        symbol="NFLX",
        open=400.0, high=410.0, low=395.0, close=405.0,
        volume=18000000, timestamp=datetime.utcnow()
    ).dict())
    db_session.add(candle)
    db_session.commit()
    db_session.refresh(candle)

    response = client.delete(f"/api/v1/candles/{candle.id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

    response = client.get("/api/v1/candles/db?symbol=NFLX")
    assert response.status_code == 200
    assert all(c["id"] != candle.id for c in response.json())

    response = client.delete(f"/api/v1/candles/{candle.id}")
    assert response.status_code == 200
    assert "error" in response.json()
