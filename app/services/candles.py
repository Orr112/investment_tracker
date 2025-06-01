from app.db.crud.pricing import bulk_upsert_price_candles
from sqlalchemy.orm import Session
from datetime import datetime

def store_candles(db, symbol: str, result):
    """
    Convert validated Alpaca price bars to DB-ready dicts
    and bulk upsert to avoid duplicates.
    """
    candle_dicts = [
        {
            "symbol": symbol,
            "timestamp": candle.t,
            "open": candle.o,
            "high": candle.h,
            "low": candle.l,
            "close": candle.c,
            "volume": candle.v,
            "created_at": datetime.utcnow(),
        }
        for candle in result.candles
    ]

    bulk_upsert_price_candles(db, candle_dicts)