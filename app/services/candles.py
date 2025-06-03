from app.db.crud.pricing import bulk_upsert_price_candles
from sqlalchemy.orm import Session
from datetime import datetime
from app.ingestion.alpaca_client import PriceCandle, PriceFetchResult



def store_candles(db, symbol: str, result: PriceFetchResult):
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
        for candle in result.candles  # ✅ note the use of .candles
    ]

    bulk_upsert_price_candles(db, candle_dicts)