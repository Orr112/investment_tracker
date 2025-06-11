from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.schemas.enums import DirectionEnum

class AlertThresholdBase(BaseModel):
    user_id: int
    email: Optional[EmailStr] = None
    symbol: str
    threshold_price: float
    direction: DirectionEnum
    phone_alert: Optional[bool] = False
    app_alert: Optional[bool] = False

 # ✅ For creating new thresholds
class AlertThresholdCreate(AlertThresholdBase):
    pass

# ✅ For updating thresholds (PATCH/PUT)
class AlertThresholdUpdate(BaseModel):
    threshold_price: Optional[float] = None
    direction:  Optional[DirectionEnum] = None
    is_triggered:  Optional[bool] = None

# ✅ For reading threshold data
class AlertThresholdOut(AlertThresholdBase):
    id: int
    is_triggered: bool
    created_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True