
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.db.models.pricing import PriceCandle as CandleModel
from app.schemas.pricing import PriceCandleCreate

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

def test_read_candles(client, db_session):
    payload = PriceCandleCreate(
        symbol="TSLA",
        open=800.0,
        high=820.0,
        low=790.0,
        close=810.0,
        volume=32100000,
        timestamp=datetime.utcnow() - timedelta(days=1)
    )
    #db_candle = db_session
    from app.db.models.pricing import PriceCandle
    candle = PriceCandle(**payload.dict())
    db_session.add(candle)
    db_session.commit()
    db_session.refresh(candle)

    # Call GET /api/v1/candles/db
    response = client.get("/api/v1/candles/db", params={"symbol":"TSLA"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["symbol"] == "TSLA" for item in data)


def test_read_candles_with_date_filtering(client, db_session):
    now = datetime.utcnow()
    candle1 = PriceCandleCreate(
        symbol="MSFT",
        open=300.0, high=310.0, low=295.0, close=305.0,
        volume=15000000,
        timestamp=now - timedelta(days=3)
    )
    candle2 = PriceCandleCreate(
        symbol="MSFT",
        open=310.0, high=320.0, low=305.0, close=315.0,
        volume=16000000,
        timestamp=now - timedelta(days=1)
    )

    # Add candles to DB
    db_session.add_all([
        CandleModel(**candle1.dict()),
        CandleModel(**candle2.dict())
    ])
    db_session.commit()

    # Case 1: start filter (should return only candle2)
    start = (now - timedelta(days=2)).isoformat()
    response = client.get(f"/api/v1/candles/db?symbol=MSFT&start={start}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["timestamp"].startswith(candle2.timestamp.date().isoformat())

    # Case 2: end filter (should return only candle1)
    end = (now - timedelta(days=2)).isoformat()
    response = client.get(f"/api/v1/candles/db?symbol=MSFT&end={end}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["timestamp"].startswith(candle1.timestamp.date().isoformat())

    # Case 3: full range (should return both)
    start = (now - timedelta(days=4)).isoformat()
    end = now.isoformat()
    response = client.get(f"/api/v1/candles/db?symbol=MSFT&start={start}&end={end}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
