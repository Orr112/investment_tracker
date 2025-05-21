from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.candles import store_candles
from datetime import datetime
from typing import List
from app.schemas.pricing import PriceCandle
from app.ingestion.alpaca_client import fetch_price_candles


router = APIRouter()

@router.get("/candles", response_model=list[PriceCandle], tags=["Candles"])
def get_candles(
    symbol: str = Query(..., description="Ticker symbol (e.g., AAPL)"),
    timeframe: str = Query(..., description="Timeframe (e.g., 1Day, 1Hour)"),
    start:datetime = Query(..., description="Start date (e.g., 2024-01-01T00:00:00)"),
    end: datetime = Query(..., description="End date (e.g., 2024-01-10T00:00:00)"),):
    candles = fetch_price_candles(symbol=symbol, timeframe=timeframe, start=start, end=end)
    return candles

@router.post("/candles/{symbol}")
def ingest_candles(symbol: str, db: Session = Depends(get_db)):
    bars = fetch_price_candles(symbol, start="2024-01-01", end="2024-05-01")
    store_candles(db, symbol, bars)
    return {"status": "ingested", "count": len(bars)}