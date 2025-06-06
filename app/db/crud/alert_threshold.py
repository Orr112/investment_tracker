from sqlalchemy.orm import Session
from app.db.models.alerts import AlertThreshold
from app.schemas.alert_threshold import AlertThresholdCreate, AlertThresholdUpdate

# ✅ Create a new alert threshold
def create_alert_threshold(db: Session, threshold: AlertThresholdCreate) -> AlertThreshold:
    db_threshold = AlertThreshold(**threshold.dict())
    db.add(db_threshold)
    db.commit()
    db.refresh(db_threshold)
    return db_threshold

# ✅ Get a threshold by ID
def get_alert_threshold(db: Session, threshold_id: int) -> AlertThreshold:
    return db.query(AlertThreshold).filter(AlertThreshold.id == threshold_id).first()

# ✅ Get all thresholds for a user
def get_alerts_by_user(db: Session, user_id: int) -> list[AlertThreshold]:
    return db.query(AlertThreshold).filter(AlertThreshold.user_id == user_id).all()

# ✅ Update a threshold
def update_alert_threshold(db: Session, threshold_id: int, update_data: AlertThresholdUpdate) -> AlertThreshold:
    threshold = get_alert_threshold(db, threshold_id)
    if not threshold:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(threshold, key, value)
    db.commit()
    db.refresh(threshold)
    return threshold

# ✅ Delete a threshold
def delete_alert_threshold(db: Session, threshold_id: int) -> dict:
    threshold = get_alert_threshold(db, threshold_id)
    if not threshold:
        return {"error": "not found"}
    db.delete(threshold)
    db.commit()
    return {"status": "deleted"}