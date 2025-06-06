from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum
from app.db.database import Base  # ✅ use the shared metadata registry
from datetime import datetime
import enum




class DirectionEnum(enum.Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"


class AlertThreshold(Base):
    __tablename__ = "alert_thresholds"


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    email = Column(String, nullable=True)
    symbol = Column(String, index=True, nullable=False)
    threshold_price = Column(Float, nullable=False)
    direction =  Column(Enum(DirectionEnum), nullable=False)
    is_triggered= Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

