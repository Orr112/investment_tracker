from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# 🔹 Shared Base Schema
class PriceCandleBase(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    symbol: str


# 🔹 Create Schema
class PriceCandleCreate(PriceCandleBase):
    pass


# 🔹 Update Schema (optional fields)
class PriceCandleUpdate(BaseModel):
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None


# 🔹 ORM-Compatible Read Schema
class PriceCandle(PriceCandleBase):
    class Config:
        orm_mode = True


# 🔹 Output Schema (includes DB-generated fields)
class PriceCandleOut(PriceCandleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
