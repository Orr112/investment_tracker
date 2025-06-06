from datetime import datetime
from app.db.models.alerts import DirectionEnum
from app.schemas.alert_threshold import AlertThresholdCreate, AlertThresholdUpdate
from app.db.models.alerts import AlertThreshold
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app

client = TestClient(app)

def test_create_alert_threshold(db_session: Session):
    data = {
        "user_id": 1,
        "email": "user@example.com",
        "symbol": "AAPL",
        "threshold_price": 150.0,
        "direction": "ABOVE"
    }
    response = client.post("/api/v1/alerts", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["symbol"] == data["symbol"]
    assert result["threshold_price"] == data["threshold_price"]
    assert result["direction"] == data["direction"]

def test_get_alert_threshold_by_id(db_session: Session):
    threshold = AlertThreshold(
        user_id=2,
        email="get_test@example.com",
        symbol="MSFT",
        threshold_price=300.0,
        direction=DirectionEnum.BELOW,
        created_at=datetime.utcnow()
    )
    db_session.add(threshold)
    db_session.commit()
    db_session.refresh(threshold)

def test_get_alerts_for_user(db_session: Session):
    user_id = 3
    for i in range(2):
        db_session.add(AlertThreshold(
            user_id=user_id,
            email=f"user{i}@example.com",
            symbol="GOOG",
            threshold_price=1000.0 + i,
            direction=DirectionEnum.ABOVE,
            created_at=datetime.utcnow()
        ))
    db_session.commit()

    response = client.get(f"/api/v1/alerts/user/{user_id}")
    assert response.status_code ==200
    results = response.json()
    assert len(results) == 2
    assert all(item["user_id"] == user_id for item in results)

def test_update_alert_threshold(db_session: Session):
    threshold = AlertThreshold(
        user_id=4,
        email="update_test@example.com",
        symbol="TSLA",
        threshold_price=700.0,
        direction=DirectionEnum.BELOW,
        created_at=datetime.utcnow()
    )
    db_session.add(threshold)
    db_session.commit()
    db_session.refresh(threshold)

    update_data = {
        "threshold_price": 720.0,
        "direction": "ABOVE"
    }

    response = client.put(f"/api/v1/alerts/{threshold.id}", json=update_data)
    assert response.status_code == 200
    result = response.json()
    assert result["threshold_price"] == 720.0
    assert result["direction"] == "ABOVE"

def test_delete_alert_threshold(db_session: Session):
    threshold = AlertThreshold(
        user_id=5,
        email="delete_test@example.com",
        symbol="AMZN",
        threshold_price=3500.0,
        direction=DirectionEnum.ABOVE,
        created_at=datetime.utcnow()
    )
    db_session.add(threshold)
    db_session.commit()
    db_session.refresh(threshold)

    response = client.delete(f"/api/v1/alerts/{threshold.id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

    response = client.get(f"/api/v1/alerts/{threshold.id}")
    assert response.status_code == 404