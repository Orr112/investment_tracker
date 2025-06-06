from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.alert_threshold import AlertThresholdCreate, AlertThresholdUpdate, AlertThresholdOut
from app.db.crud import alert_threshold as crud
from app.db.models.alerts import AlertThreshold  # ✅ Needed for get_alert_by_id

router = APIRouter()

# 🔹 Create
@router.post("/alerts", response_model=AlertThresholdOut)
def create_alert(alert: AlertThresholdCreate, db: Session = Depends(get_db)):
    return crud.create_alert_threshold(db, alert)

# 🔹 Read (all alerts for a given user)
@router.get("/alerts/user/{user_id}", response_model=list[AlertThresholdOut])
def get_alerts_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_alerts_by_user(db, user_id=user_id)

# 🔹 Read (alert by ID)
@router.get("/alerts/{alert_id}", response_model=AlertThresholdOut)
def get_alert_by_id(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(AlertThreshold).filter(AlertThreshold.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

# 🔹 Update
@router.put("/alerts/{alert_id}", response_model=AlertThresholdOut)
def update_alert(alert_id: int, update: AlertThresholdUpdate, db: Session = Depends(get_db)):
    return crud.update_alert_threshold(db, alert_id, update)

# 🔹 Delete
@router.delete("/alerts/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    return crud.delete_alert_threshold(db, threshold_id=alert_id)
