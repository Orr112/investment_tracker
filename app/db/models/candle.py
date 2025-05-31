from sqlalchemy import Column, DateTime, Float, Integer, String
from app.db.database import Base

class Candle(Base):
    __tablename__ = "price_candle"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String,  index=True)
    timestamp = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    