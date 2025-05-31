import os
import logging
import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv


load_dotenv()


# ✅ Load API credentials from environment variables
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")
BASE_URL = os.getenv("ALPACA_BASE_URL", "https://data.alpaca.markets/v2")


# ✅ Schema for each price bar (candle)
class PriceCandle(BaseModel):
    t: datetime                     # timestamp
    o: float = Field(gt=0)          # open price
    h: float = Field(gt=0)          # high price
    l: float = Field(gt=0)          # low price
    c: float = Field(gt=0)          # close price
    v: int = Field(ge=0)            # volume (non-negative)


# ✅ Schema for full API response
class PriceFetchResult(BaseModel):
    symbol: str
    candles: List[PriceCandle]


def fetch_price_candles(symbol: str, start: str, end: str, timeframe: str = "1Day") -> PriceFetchResult:
    """
    Fetch historical price candles from Alpaca.
    Validates and returns structured results.
    """
    headers = {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_API_SECRET
    }

    url = f"{BASE_URL}/stocks/{symbol}/bars"
    params = {
        "start": start if isinstance(start, str) else start.isoformat() + "Z",
        "end": end if isinstance(end, str) else end.isoformat() + "Z",
        "timeframe": timeframe,
        "limit": 1000
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"Alpaca API error: {response.status_code} {response.text}")
        raise Exception("Failed to fetch data from Alpaca")

    try:
        raw_bars = response.json().get("bars", [])
        candles = [PriceCandle(**bar) for bar in raw_bars]
        return PriceFetchResult(symbol=symbol, candles=candles)
    except ValidationError as e:
        logging.error(f"Data validation failed for {symbol}: {e}")
        raise
