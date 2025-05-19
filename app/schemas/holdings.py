from pydantic import BaseModel, Field 
from typing import Optional
from datetime import datetime

class HoldingBase(BaseModel):
    symbol: str = Field(..., example="APPL")
    quantity: float = Field(..., gt=0, example=10.5)
    purchase_price: float = Field(..., gt=0, example=150.00)

class HoldingCreate(HoldingBase):
    purchase_date: datetime

class HoldingUpdate(BaseModel):
    symbol: Optional[str] = Field(None, example="APPL")
    quantity: Optional[float] = Field(None, gt=0, example=12.0)
    purchase_price: Optional[float] = Field(None, gt=0, example=145.00)
    current_price: float | None = None

class HoldingOut(HoldingBase):
    id: int
    symbol: str
    quantity: float = Field(..., alias="shares")
    purchase_price: float
    purchase_date: datetime
    current_price: float | None = None
    auto_sell_triggered: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True