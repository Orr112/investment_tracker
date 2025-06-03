from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class PriceCandle(BaseModel):
    t: datetime
    o: float = Field(gt=0)
    h: float = Field(gt=0)
    l: float = Field(gt=0)
    c: float = Field(gt=0)
    v: int = Field(ge=0)

class PriceFetchResult(BaseModel):
    symbol: str
    candles: List[PriceCandle]
