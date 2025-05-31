from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PriceCandleBase(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    symbol: str 

class PriceCandleOut(PriceCandleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PriceCandleCreate(PriceCandleBase):
    pass 


class PriceCandleUpdate(BaseModel):
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None

class PriceCandle(PriceCandleBase):
    class Config:
        orm_mode = True   
    
