from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.candles import store_candles
from datetime import datetime
from typing import List, Optional
from app.schemas.pricing import PriceCandle
from app.ingestion.alpaca_client import fetch_price_candles
import app.db.crud.pricing as crud
from app.schemas.pricing import PriceCandle, PriceCandleCreate, PriceCandleUpdate


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

@router.post("/candles", response_model=PriceCandle, tags=["Candles"])
def create_candle(candle: PriceCandleCreate, db: Session = Depends(get_db)):
    return crud.create_price_candle(db, candle)

@router.get("/candles/db", response_model=List[PriceCandle], tags=["Candles"])
def read_candles(
    symbol: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    return crud.get_price_candles(db, symbol, start=start, end=end)

@router.put("/candles/{candle_id}", response_model=PriceCandle, tags=["Candles"])
def update_candle(candle_id: int, update: PriceCandleUpdate, db: Session = Depends(get_db)):
    return crud.update_price_candle(db, candle_id, update)

@router.delete("/candles/{candle_id}", tags=["Candles"])
def delete_candle(candle_id: int, db: Session = Depends(get_db)):
    return crud.delete_price_candle(db, candle_id)