
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


def test_get_price_candle_by_id(client, db_session):
    # Create a new candle
    candle_data = PriceCandleCreate(
        symbol="NFLX",
        open=400.0,
        high=410.0,
        low=390.0,
        close=405.0,
        volume=17000000,
        timestamp=datetime.utcnow() - timedelta(days=1)
    )
    candle = CandleModel(**candle_data.dict())
    db_session.add(candle)
    db_session.commit()
    db_session.refresh(candle)

    # GET the candle by ID
    response = client.get(f"/api/v1/candles/{candle.id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == candle.id
    assert data["symbol"] == candle.symbol
    assert data["open"] == candle.open
    assert data["high"] == candle.high
    assert data["low"] == candle.low
    assert data["close"] == candle.close
    assert data["volume"] == candle.volume


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


def test_update_candle(client, db_session):
    # 1. Create initial candle in DB
    payload = PriceCandleCreate(
        symbol="AMZN",
        open=100.0, high=105.0, low=98.0, close=102.0,
        volume=10000000,
        timestamp=datetime.utcnow()
    )
    db_candle = CandleModel(**payload.dict())
    db_session.add(db_candle)
    db_session.commit()
    db_session.refresh(db_candle)

    #2.  Prepare update data

    update_data = {
        "close": 103.5,
        "volume": 11000000
    }
    # 3. Call update endpoint
    response = client.put(f"/api/v1/candles/{db_candle.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()

    # 4. Verify update
    assert data["id"] == db_candle.id
    assert data["close"] == update_data["close"]
    assert data["volume"] == update_data["volume"]
    assert data["symbol"] == payload.symbol

def test_delete_candle(client, db_session):
    # Step 1: Create a candle
    candle_data = PriceCandleCreate(
        symbol="NFLX",
        open=400.0, high=410.0, low=395.0, close=405.0,
        volume=18000000,
        timestamp=datetime.utcnow()
    )
    candle_model = CandleModel(**candle_data.dict())
    db_session.add(candle_model)
    db_session.commit()
    db_session.refresh(candle_model)

    candle_id = candle_model.id

    # Step 2: Delete the candle
    response = client.delete(f"/api/v1/candles/{candle_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"
    assert response.json()["id"] == candle_id

    # Step 3: Confirm it's gone
    response = client.get(f"/api/v1/candles/db?symbol=NFLX")
    assert response.status_code == 200
    data = response.json()
    assert all(c["id"] != candle_id for c in data)

    # Step 4: Try deleting again expect an error
    response = client.delete(f"/api/v1/candles/{candle_id}")
    assert response.status_code == 200
    assert "error" in response.json()