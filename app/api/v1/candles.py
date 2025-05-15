from fastapi import APIRouter, Query
from datetime import datetime
from typing import List
from app.schemas.pricing import PriceCandle
from app.services.candles import fetch_price_candles

router = APIRouter()

@router.get("/candles", response_model=list[PriceCandle], tags=["Candles"])
def get_candles(
    symbol: str = Query(..., description="Ticker symbol (e.g., AAPL)"),
    timeframe: str = Query(..., description="Timeframe (e.g., 1Day, 1Hour)"),
    start:datetime = Query(..., description="Start date (e.g., 2024-01-01T00:00:00)"),
    end: datetime = Query(..., description="End date (e.g., 2024-01-10T00:00:00)"),):
    candles = fetch_price_candles(symbol=symbol, timeframe=timeframe, start=start, end=end)
    return candles