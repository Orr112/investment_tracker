from pydantic import BaseModel, Field 
from typing import Optional
from datetime import datetime

class HoldingBase(BaseModel):
    symbol: str = Field(..., example="AAPL")
    quantity: float = Field(..., gt=0, example=10.5)
    purchase_price: float = Field(..., gt=0, example=150.00)

class HoldingCreate(HoldingBase):
    pass 

class HoldingUpdate(BaseModel):
    symbol: Optional[str] = Field(None, example="AAPL")
    quantity: Optional[float] = Field(None, gt=0, example=12.0)
    purchase_price: Optional[float] = Field(None, gt=0, example=145.00)

class HoldingOut(HoldingBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True